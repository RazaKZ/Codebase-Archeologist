"""
Agent 3: Business Logic Extractor
Uses AI to reverse engineer code intent and add natural language descriptions
"""
from typing import Dict, List, Optional, Tuple
import httpx
from config.settings import settings

class BusinessLogicExtractor:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.LLM_MODEL
        self.cache = {}  # Simple in-memory cache
    
    async def extract_logic(self, nodes: List[Dict], code_context: Dict) -> List[Dict]:
        """
        Extract business logic descriptions for code nodes
        
        Args:
            nodes: List of code nodes (functions, classes)
            code_context: Additional context about the codebase
        
        Returns:
            Annotated nodes with descriptions and confidence scores
        """
        annotated_nodes = []
        
        for node in nodes:
            # Check cache first
            cache_key = f"{node['id']}_{node.get('name', '')}"
            if cache_key in self.cache:
                annotated_nodes.append(self.cache[cache_key])
                continue
            
            # Extract description using AI
            description, confidence = await self._get_ai_description(node, code_context)
            
            annotated_node = {
                **node,
                "description": description,
                "confidence": confidence,
                "business_logic": self._extract_business_keywords(description)
            }
            
            annotated_nodes.append(annotated_node)
            self.cache[cache_key] = annotated_node
        
        return annotated_nodes
    
    async def _get_ai_description(self, node: Dict, context: Dict) -> Tuple[str, float]:
        """
        Get AI-generated description for a code node
        
        Returns:
            Tuple of (description, confidence_score)
        """
        # Fallback mode if no API key
        if not self.api_key:
            return self._fallback_description(node), 0.5
        
        try:
            # Use Gemini API
            prompt = self._build_prompt(node, context)
            description = await self._call_gemini(prompt)
            confidence = self._calculate_confidence(description, node)
            return description, confidence
        except Exception as e:
            # Fallback on error
            return self._fallback_description(node), 0.3
    
    def _build_prompt(self, node: Dict, context: Dict) -> str:
        """Build prompt for AI analysis"""
        return f"""
Analyze this code element and provide a clear, concise description of what it does:

Type: {node.get('type', 'unknown')}
Name: {node.get('name', 'unknown')}
File: {node.get('file', 'unknown')}
Lines: {node.get('line_start', '?')}-{node.get('line_end', '?')}

Context: This is part of a {context.get('project_type', 'software')} project.

Provide a one-sentence description of what this code does, focusing on its business purpose.
Be specific and avoid generic descriptions.
"""
    
    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API"""
        if not self.api_key:
            return "Unable to analyze: API key not configured"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}",
                    json={
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }],
                        "generationConfig": {
                            "temperature": settings.LLM_TEMPERATURE,
                            "maxOutputTokens": settings.LLM_MAX_TOKENS
                        }
                    },
                    timeout=30.0
                )
                if response.status_code == 200:
                    data = response.json()
                    if 'candidates' in data and len(data['candidates']) > 0:
                        return data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            pass
        
        return "Analysis unavailable"
    
    def _calculate_confidence(self, description: str, node: Dict) -> float:
        """Calculate confidence score for AI description"""
        # Simple heuristic: longer, more specific descriptions = higher confidence
        if not description or description == "Analysis unavailable":
            return 0.0
        
        confidence = 0.5  # Base confidence
        
        # Increase confidence for specific keywords
        specific_keywords = ['validates', 'processes', 'handles', 'manages', 'calculates', 'transforms']
        if any(kw in description.lower() for kw in specific_keywords):
            confidence += 0.2
        
        # Increase confidence for longer descriptions
        if len(description) > 50:
            confidence += 0.2
        
        # Decrease confidence for generic descriptions
        generic_phrases = ['this function', 'this code', 'does something']
        if any(phrase in description.lower() for phrase in generic_phrases):
            confidence -= 0.2
        
        return min(1.0, max(0.0, confidence))
    
    def _fallback_description(self, node: Dict) -> str:
        """Generate fallback description without AI"""
        node_type = node.get('type', 'element')
        name = node.get('name', 'unknown')
        
        # Simple heuristics based on naming
        if 'validate' in name.lower() or 'check' in name.lower():
            return f"This {node_type} validates or checks {name}"
        elif 'process' in name.lower() or 'handle' in name.lower():
            return f"This {node_type} processes or handles {name}"
        elif 'get' in name.lower() or 'fetch' in name.lower():
            return f"This {node_type} retrieves {name}"
        elif 'set' in name.lower() or 'update' in name.lower():
            return f"This {node_type} updates {name}"
        else:
            return f"This {node_type} implements {name}"
    
    def _extract_business_keywords(self, description: str) -> List[str]:
        """Extract business-relevant keywords from description"""
        keywords = []
        business_terms = [
            'payment', 'user', 'authentication', 'authorization', 'validation',
            'transaction', 'order', 'product', 'customer', 'invoice', 'report',
            'notification', 'email', 'sms', 'api', 'database', 'cache'
        ]
        
        description_lower = description.lower()
        for term in business_terms:
            if term in description_lower:
                keywords.append(term)
        
        return keywords

