"""
Agent 5: Orchestrator
Manages state between agents, handles errors, caches results, streams progress
"""
from typing import Dict, Optional, AsyncGenerator
import asyncio

from agents.repo_analyzer import RepoAnalyzer
from agents.dependency_mapper import DependencyMapper
from agents.business_logic_extractor import BusinessLogicExtractor
from agents.impact_analyzer import ImpactAnalyzer
from core.websocket_manager import ConnectionManager

class AnalysisState:
    """State object for the analysis workflow"""
    def __init__(self):
        self.repo_url: Optional[str] = None
        self.ast_data: Optional[Dict] = None
        self.graph_data: Optional[Dict] = None
        self.annotated_nodes: Optional[list] = None
        self.impact_analysis: Optional[Dict] = None
        self.errors: list = []
        self.progress: float = 0.0
        self.current_agent: Optional[str] = None

class Orchestrator:
    def __init__(self, ws_manager: Optional[ConnectionManager] = None, client_id: Optional[str] = None):
        self.repo_analyzer = RepoAnalyzer()
        self.dependency_mapper = DependencyMapper()
        self.business_extractor = BusinessLogicExtractor()
        self.ws_manager = ws_manager
        self.client_id = client_id
        self.cache = {}
    
    async def analyze(self, repo_url: str, impact_target: Optional[str] = None) -> AsyncGenerator[Dict, None]:
        """
        Orchestrate the full analysis workflow
        
        Args:
            repo_url: Repository URL to analyze
            impact_target: Optional node ID for impact analysis
        
        Yields:
            Progress updates and results
        """
        state = AnalysisState()
        state.repo_url = repo_url
        
        try:
            # Agent 1: Repo Analyzer
            await self._send_progress("Repo Analyzer", 0.1, "Cloning repository and extracting AST...")
            state.ast_data = await self.repo_analyzer.analyze_repo(repo_url)
            yield {"agent": "repo_analyzer", "status": "completed", "data": state.ast_data}
            
            # Agent 2: Dependency Mapper
            await self._send_progress("Dependency Mapper", 0.3, "Building dependency graph...")
            state.graph_data = self.dependency_mapper.build_graph(state.ast_data)
            yield {"agent": "dependency_mapper", "status": "completed", "data": state.graph_data}
            
            # Agent 3: Business Logic Extractor
            await self._send_progress("Business Logic Extractor", 0.6, "Extracting business logic...")
            state.annotated_nodes = await self.business_extractor.extract_logic(
                state.graph_data["nodes"],
                {"project_type": "software"}
            )
            yield {"agent": "business_extractor", "status": "completed", "data": state.annotated_nodes}
            
            # Agent 4: Impact Analyzer (if target provided)
            if impact_target:
                await self._send_progress("Impact Analyzer", 0.8, f"Analyzing impact of {impact_target}...")
                impact_analyzer = ImpactAnalyzer(self.dependency_mapper.graph)
                state.impact_analysis = impact_analyzer.analyze_impact(impact_target)
                yield {"agent": "impact_analyzer", "status": "completed", "data": state.impact_analysis}
            
            await self._send_progress("Orchestrator", 1.0, "Analysis complete!")
            yield {
                "agent": "orchestrator",
                "status": "completed",
                "summary": {
                    "total_files": state.ast_data.get("total_files", 0),
                    "total_functions": state.ast_data.get("total_functions", 0),
                    "total_classes": state.ast_data.get("total_classes", 0),
                    "graph_nodes": len(state.graph_data.get("nodes", [])),
                    "graph_edges": len(state.graph_data.get("edges", []))
                }
            }
        
        except Exception as e:
            state.errors.append(str(e))
            await self._send_progress("Error", 0.0, f"Error: {str(e)}")
            yield {"agent": "error", "status": "failed", "error": str(e)}
    
    async def _send_progress(self, agent: str, progress: float, message: str):
        """Send progress update via WebSocket if available"""
        if self.ws_manager and self.client_id:
            await self.ws_manager.send_progress(self.client_id, agent, progress, message)
    
    def get_cached_result(self, repo_url: str) -> Optional[Dict]:
        """Get cached analysis result"""
        return self.cache.get(repo_url)
    
    def cache_result(self, repo_url: str, result: Dict):
        """Cache analysis result"""
        self.cache[repo_url] = result

