"""
Chat API routes for codebase assistant
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
import httpx
import json

from database.database import get_db
from database.models import Project, Analysis
from config.settings import settings

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    project_id: Optional[int] = None
    analysis_results: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    context_used: bool

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Chat with AI assistant about codebase"""
    try:
        # Get analysis results if project_id is provided
        analysis_context = ""
        if request.project_id:
            project = db.query(Project).filter(Project.id == request.project_id).first()
            if project:
                analyses = db.query(Analysis).filter(
                    Analysis.project_id == request.project_id,
                    Analysis.status == "completed"
                ).all()
                
                # Build context from analysis results
                context_parts = []
                for analysis in analyses:
                    if analysis.agent_name == "repo_analyzer" and analysis.result:
                        result = analysis.result
                        context_parts.append(f"Repository Analysis:\n- Total Files: {result.get('total_files', 0)}\n- Total Functions: {result.get('total_functions', 0)}\n- Total Classes: {result.get('total_classes', 0)}")
                    
                    elif analysis.agent_name == "dependency_mapper" and analysis.result:
                        result = analysis.result
                        nodes_count = len(result.get('nodes', []))
                        edges_count = len(result.get('edges', []))
                        analysis_data = result.get('analysis', {})
                        context_parts.append(f"Dependency Graph:\n- Nodes: {nodes_count}\n- Edges: {edges_count}\n- Dead Functions: {len(analysis_data.get('dead_functions', []))}\n- Circular Dependencies: {len(analysis_data.get('circular_dependencies', []))}\n- High Coupling: {len(analysis_data.get('high_coupling', []))}")
                
                if context_parts:
                    analysis_context = "\n\n".join(context_parts)
        
        # Also use provided analysis_results if available
        if request.analysis_results:
            context_parts = []
            if request.analysis_results.get('repo_analyzer'):
                repo_data = request.analysis_results['repo_analyzer']
                context_parts.append(f"Repository: {repo_data.get('total_files', 0)} files, {repo_data.get('total_functions', 0)} functions")
            
            if request.analysis_results.get('dependency_mapper'):
                dep_data = request.analysis_results['dependency_mapper']
                context_parts.append(f"Dependency Graph: {len(dep_data.get('nodes', []))} nodes, {len(dep_data.get('edges', []))} edges")
            
            if context_parts:
                analysis_context = (analysis_context + "\n\n" + "\n".join(context_parts)) if analysis_context else "\n".join(context_parts)
        
        # Build prompt with context
        if analysis_context:
            prompt = f"""You are a helpful codebase analysis assistant. You have access to the following analysis results:

{analysis_context}

User Question: {request.message}

Provide a helpful, concise answer. If the question is about the codebase structure, dependencies, or code quality, use the analysis data provided. If it's a general question, answer normally. Be friendly and professional."""
        else:
            prompt = f"""You are a helpful codebase analysis assistant. The user is asking: {request.message}

Provide a helpful, concise answer. Be friendly and professional."""

        # Call Gemini API
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY.strip() == "":
            # Fallback response without API
            fallback_responses = {
                "hello": "Hello! I'm your codebase assistant. I can help you understand your codebase structure, dependencies, and code quality metrics.",
                "analysis": "Based on the analysis results, I can see information about your codebase structure, dependencies, and code quality.",
                "repo": "I can help you understand your repository structure, dependencies between files, and identify code quality issues."
            }
            
            message_lower = request.message.lower()
            for key, response in fallback_responses.items():
                if key in message_lower:
                    return ChatResponse(
                        response=response + " However, the AI assistant is not fully configured. Please set up the Gemini API key in the backend .env file for full AI-powered responses.",
                        context_used=bool(analysis_context)
                    )
            
            return ChatResponse(
                response="I'm here to help! However, the AI assistant needs a Gemini API key to be configured. Please add GEMINI_API_KEY to your backend .env file. For now, I can tell you that analysis results are available in the dashboard.",
                context_used=False
            )

        async with httpx.AsyncClient() as client:
            try:
                # Use the model from settings (default: gemini-1.5-flash)
                model_name = settings.LLM_MODEL
                
                # API endpoint
                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
                
                response = await client.post(
                    api_url,
                    json={
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }],
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 1000
                        }
                    },
                    timeout=30.0
                )
                
                # If 404, try alternative models
                if response.status_code == 404:
                    # Try gemini-1.5-pro as fallback
                    fallback_models = ["gemini-1.5-pro", "gemini-pro"]
                    for fallback_model in fallback_models:
                        if fallback_model != model_name:
                            try:
                                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{fallback_model}:generateContent?key={settings.GEMINI_API_KEY}"
                                response = await client.post(
                                    api_url,
                                    json={
                                        "contents": [{
                                            "parts": [{"text": prompt}]
                                        }],
                                        "generationConfig": {
                                            "temperature": 0.7,
                                            "maxOutputTokens": 1000
                                        }
                                    },
                                    timeout=30.0
                                )
                                if response.status_code == 200:
                                    break
                            except:
                                continue

                if response.status_code == 200:
                    data = response.json()
                    if 'candidates' in data and len(data['candidates']) > 0:
                        candidate = data['candidates'][0]
                        if 'content' in candidate and 'parts' in candidate['content']:
                            ai_response = candidate['content']['parts'][0].get('text', '')
                            if ai_response:
                                return ChatResponse(
                                    response=ai_response,
                                    context_used=bool(analysis_context)
                                )
                    
                    # Check for errors in response
                    if 'error' in data:
                        error_msg = data['error'].get('message', 'Unknown error')
                        return ChatResponse(
                            response=f"I encountered an error: {error_msg}. Please check your Gemini API key configuration.",
                            context_used=False
                        )
                
                # Non-200 status code
                error_text = response.text
                return ChatResponse(
                    response=f"I'm sorry, I couldn't process your request. API returned status {response.status_code}. Please check your Gemini API key and try again.",
                    context_used=False
                )
            
            except httpx.TimeoutException:
                return ChatResponse(
                    response="The request timed out. Please try again with a shorter question.",
                    context_used=False
                )
            except httpx.RequestError as e:
                return ChatResponse(
                    response=f"Network error: {str(e)}. Please check your internet connection and API configuration.",
                    context_used=False
                )

    except Exception as e:
        # Log the error for debugging
        import logging
        logging.error(f"Chat error: {str(e)}")
        return ChatResponse(
            response=f"I encountered an error: {str(e)}. Please check the backend logs for more details.",
            context_used=False
        )

