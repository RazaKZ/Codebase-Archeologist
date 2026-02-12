"""
Agent 4: Impact Analyzer
Analyzes what breaks if a component is deleted or modified
"""
from typing import Dict, List, Set, Tuple
import networkx as nx

class ImpactAnalyzer:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
    
    def analyze_impact(self, target_node_id: str, action: str = "delete") -> Dict:
        """
        Analyze impact of deleting or modifying a node
        
        Args:
            target_node_id: ID of the node to analyze
            action: "delete" or "modify"
        
        Returns:
            Impact analysis report
        """
        if target_node_id not in self.graph:
            return {
                "error": f"Node {target_node_id} not found in graph",
                "risk": "UNKNOWN"
            }
        
        # Find all affected nodes
        affected_nodes = self._find_affected_nodes(target_node_id)
        
        # Calculate risk rating
        risk = self._calculate_risk(target_node_id, affected_nodes)
        
        # Generate report
        report = self._generate_report(target_node_id, affected_nodes, risk, action)
        
        return {
            "target_node": target_node_id,
            "action": action,
            "affected_nodes": list(affected_nodes),
            "affected_count": len(affected_nodes),
            "risk_rating": risk,
            "report": report,
            "visualization": self._generate_visualization_data(target_node_id, affected_nodes)
        }
    
    def _find_affected_nodes(self, target_node_id: str) -> Set[str]:
        """Find all nodes that would be affected by deleting target_node"""
        affected = set()
        
        # Forward traversal: nodes that depend on target
        if self.graph.has_node(target_node_id):
            # Find all descendants (nodes reachable from target)
            descendants = set(nx.descendants(self.graph, target_node_id))
            affected.update(descendants)
            
            # Find all ancestors (nodes that target depends on)
            ancestors = set(nx.ancestors(self.graph, target_node_id))
            
            # Nodes that would break if target is deleted
            # (nodes that have target as their only dependency)
            for node in self.graph.nodes():
                if node == target_node_id:
                    continue
                predecessors = list(self.graph.predecessors(node))
                if target_node_id in predecessors and len(predecessors) == 1:
                    affected.add(node)
        
        return affected
    
    def _calculate_risk(self, target_node_id: str, affected_nodes: Set[str]) -> str:
        """Calculate risk rating: HIGH, MEDIUM, or LOW"""
        if not self.graph.has_node(target_node_id):
            return "UNKNOWN"
        
        node_data = self.graph.nodes[target_node_id]
        in_degree = self.graph.in_degree(target_node_id)
        out_degree = self.graph.out_degree(target_node_id)
        
        # High risk factors
        if len(affected_nodes) > 20:
            return "HIGH"
        if in_degree > 10:  # Many things depend on this
            return "HIGH"
        if node_data.get('type') == 'class' and out_degree > 5:
            return "HIGH"
        
        # Medium risk factors
        if len(affected_nodes) > 5:
            return "MEDIUM"
        if in_degree > 3:
            return "MEDIUM"
        
        # Low risk
        return "LOW"
    
    def _generate_report(self, target_node_id: str, affected_nodes: Set[str], risk: str, action: str) -> str:
        """Generate markdown report"""
        node_data = self.graph.nodes[target_node_id]
        node_name = node_data.get('name', target_node_id)
        node_type = node_data.get('type', 'element')
        
        report = f"""# Impact Analysis Report

## Target: {node_name} ({node_type})

**Action**: {action.capitalize()}
**Risk Rating**: **{risk}**

### Summary
{action.capitalize()}ing this {node_type} will affect **{len(affected_nodes)}** other components.

### Affected Components
"""
        
        if affected_nodes:
            for i, node_id in enumerate(list(affected_nodes)[:20], 1):  # Limit to 20
                if self.graph.has_node(node_id):
                    affected_data = self.graph.nodes[node_id]
                    report += f"{i}. `{affected_data.get('name', node_id)}` ({affected_data.get('type', 'unknown')}) in `{affected_data.get('file', 'unknown')}`\n"
            
            if len(affected_nodes) > 20:
                report += f"\n... and {len(affected_nodes) - 20} more components.\n"
        else:
            report += "No other components are directly affected.\n"
        
        report += f"\n### Recommendations\n"
        
        if risk == "HIGH":
            report += "- ⚠️ **High Risk**: This component is critical. Consider refactoring dependencies before deletion.\n"
            report += "- Review all affected components before proceeding.\n"
            report += "- Create comprehensive tests for affected areas.\n"
        elif risk == "MEDIUM":
            report += "- ⚠️ **Medium Risk**: This component has moderate dependencies. Proceed with caution.\n"
            report += "- Update dependent components after deletion.\n"
        else:
            report += "- ✅ **Low Risk**: This component has minimal dependencies. Safe to proceed.\n"
        
        return report
    
    def _generate_visualization_data(self, target_node_id: str, affected_nodes: Set[str]) -> Dict:
        """Generate data for visualization"""
        # Get subgraph of affected nodes
        nodes_to_include = {target_node_id} | affected_nodes
        
        subgraph = self.graph.subgraph(nodes_to_include)
        
        return {
            "nodes": [
                {
                    "id": node_id,
                    "is_target": node_id == target_node_id,
                    **self.graph.nodes[node_id]
                }
                for node_id in subgraph.nodes()
            ],
            "edges": [
                {
                    "source": source,
                    "target": target
                }
                for source, target in subgraph.edges()
            ]
        }

