"""
Analysis API routes
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import Optional, Dict, List
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Project, Analysis
from agents.orchestrator import Orchestrator
from core.websocket_manager import ConnectionManager

router = APIRouter()

class AnalysisRequest(BaseModel):
    repo_url: str
    impact_target: Optional[str] = None
    client_id: Optional[str] = None

class AnalysisResponse(BaseModel):
    project_id: int
    status: str
    message: str

@router.post("/start", response_model=AnalysisResponse)
async def start_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start a new analysis"""
    try:
        # Create or get project
        project = db.query(Project).filter(Project.repo_url == request.repo_url).first()
        if not project:
            project = Project(
                name=request.repo_url.split("/")[-1],
                repo_url=request.repo_url,
                status="pending"
            )
            db.add(project)
            db.commit()
            db.refresh(project)
        
        # Start analysis in background
        ws_manager = ConnectionManager()
        orchestrator = Orchestrator(ws_manager, request.client_id)
        
        background_tasks.add_task(
            run_analysis,
            project.id,
            request.repo_url,
            request.impact_target,
            orchestrator,
            None
        )
        
        return AnalysisResponse(
            project_id=project.id,
            status="started",
            message="Analysis started"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def run_analysis(
    project_id: int,
    repo_url: str,
    impact_target: Optional[str],
    orchestrator: Orchestrator,
    db_session_factory
):
    """Run analysis and save results"""
    from database.database import SessionLocal
    db = SessionLocal()
    try:
        # Update project status
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.status = "analyzing"
            db.commit()
        
        # Run analysis
        results = {}
        async for result in orchestrator.analyze(repo_url, impact_target):
            agent = result.get("agent")
            if agent and agent != "error":
                # Save analysis result
                analysis = Analysis(
                    project_id=project_id,
                    agent_name=agent,
                    status="completed",
                    result=result.get("data"),
                    confidence_score=0.8
                )
                db.add(analysis)
                db.commit()
                results[agent] = result.get("data")
        
        # Update project status
        if project:
            project.status = "completed"
            db.commit()
        
        # Cache result
        orchestrator.cache_result(repo_url, results)
    
    except Exception as e:
        # Update project status on error
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.status = "failed"
            db.commit()
        
        # Save error
        analysis = Analysis(
            project_id=project_id,
            agent_name="orchestrator",
            status="failed",
            error=str(e)
        )
        db.add(analysis)
        db.commit()
    finally:
        db.close()

@router.get("/status/{project_id}")
async def get_analysis_status(project_id: int, db: Session = Depends(get_db)):
    """Get analysis status"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    analyses = db.query(Analysis).filter(Analysis.project_id == project_id).all()
    
    return {
        "project_id": project.id,
        "status": project.status,
        "analyses": [
            {
                "agent": a.agent_name,
                "status": a.status,
                "confidence": a.confidence_score
            }
            for a in analyses
        ]
    }

@router.get("/results/{project_id}")
async def get_analysis_results(project_id: int, db: Session = Depends(get_db)):
    """Get analysis results"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    analyses = db.query(Analysis).filter(
        Analysis.project_id == project_id,
        Analysis.status == "completed"
    ).all()
    
    results = {}
    for analysis in analyses:
        results[analysis.agent_name] = analysis.result
    
    return {
        "project_id": project.id,
        "repo_url": project.repo_url,
        "results": results
    }

@router.post("/impact")
async def analyze_impact(
    request: Dict,
    db: Session = Depends(get_db)
):
    """Analyze impact of deleting/modifying a component"""
    project_id = request.get("project_id")
    target_node = request.get("target_node")
    
    if not project_id or not target_node:
        raise HTTPException(status_code=400, detail="project_id and target_node required")
    
    # Get graph data from previous analysis
    analysis = db.query(Analysis).filter(
        Analysis.project_id == project_id,
        Analysis.agent_name == "dependency_mapper"
    ).first()
    
    if not analysis or not analysis.result:
        raise HTTPException(status_code=404, detail="Dependency graph not found")
    
    # Rebuild graph and analyze impact
    from agents.dependency_mapper import DependencyMapper
    from agents.impact_analyzer import ImpactAnalyzer
    import networkx as nx
    
    mapper = DependencyMapper()
    # Reconstruct graph from saved data
    graph_data = analysis.result
    for node in graph_data.get("nodes", []):
        mapper.graph.add_node(node["id"], **{k: v for k, v in node.items() if k != "id"})
    for edge in graph_data.get("edges", []):
        mapper.graph.add_edge(edge["source"], edge["target"])
    
    analyzer = ImpactAnalyzer(mapper.graph)
    impact = analyzer.analyze_impact(target_node)
    
    return impact

