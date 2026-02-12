"""
Agent 2: Dependency Mapper
Builds dependency graphs and identifies issues (dead code, circular deps, hotspots)
"""
import networkx as nx
from typing import Dict, List, Tuple
from collections import defaultdict

class DependencyMapper:
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def build_graph(self, ast_data: Dict) -> Dict:
        """
        Build dependency graph from AST data
        
        Args:
            ast_data: Output from RepoAnalyzer
        
        Returns:
            Graph with nodes, edges, and analysis results
        """
        self.graph.clear()
        
        # Add nodes
        for node in ast_data['nodes']:
            self.graph.add_node(
                node['id'],
                **{k: v for k, v in node.items() if k != 'id'}
            )
        
        # Add edges based on imports and function calls
        edges = []
        imports = ast_data.get('imports', {})
        
        # Group nodes by file
        nodes_by_file = defaultdict(list)
        for node in ast_data['nodes']:
            file_path = node.get('file', '')
            nodes_by_file[file_path].append(node)
        
        # 1. Create edges between functions in the same file (create a chain)
        for file_path, file_nodes in nodes_by_file.items():
            if len(file_nodes) < 2:
                continue
            # Sort by line number
            sorted_nodes = sorted(file_nodes, key=lambda n: n.get('line_start', 0))
            # Connect each function to the next one (sequential flow)
            for i in range(len(sorted_nodes) - 1):
                source_id = sorted_nodes[i]['id']
                target_id = sorted_nodes[i + 1]['id']
                if source_id in self.graph and target_id in self.graph:
                    edges.append((source_id, target_id))
            # Also connect last to first to show they're related (optional, creates a cycle indicator)
            # Uncomment if you want circular connections within files
            # if len(sorted_nodes) > 2:
            #     edges.append((sorted_nodes[-1]['id'], sorted_nodes[0]['id']))
        
        # 2. Create edges based on function name patterns (smarter heuristic)
        # Connect functions with related names (e.g., getProduct -> displayProduct -> deleteProduct)
        for source_node in ast_data['nodes']:
            if source_node.get('type') != 'function':
                continue
                
            source_name = source_node.get('name', '').lower()
            source_file = source_node.get('file', '')
            
            # Extract base name (e.g., "getProduct" -> "product")
            base_words = [w for w in source_name.replace('get', '').replace('set', '').replace('delete', '').replace('update', '').replace('display', '').replace('show', '').replace('save', '').replace('load', '').split() if len(w) > 2]
            
            for target_node in ast_data['nodes']:
                if target_node.get('type') != 'function':
                    continue
                    
                # Skip self or same file (already connected by sequential order)
                if source_node['id'] == target_node['id'] or source_node.get('file') == target_node.get('file'):
                    continue
                
                target_name = target_node.get('name', '').lower()
                
                # Connect if they share a common base word (e.g., both have "product")
                for base_word in base_words:
                    if base_word in target_name and len(base_word) > 3:
                        if source_node['id'] in self.graph and target_node['id'] in self.graph:
                            edges.append((source_node['id'], target_node['id']))
                        break
        
        # 3. Map imports to nodes (original logic, improved)
        for file_path, import_list in imports.items():
            for imp in import_list:
                # Find nodes that match this import
                for node in ast_data['nodes']:
                    node_id = node['id']
                    # Match by import name in node name or file
                    if (imp.lower() in node.get('name', '').lower() or 
                        imp.lower() in node.get('file', '').lower() or
                        node.get('file', '') == imp):
                        # Connect all nodes in the importing file to the imported node
                        for source_node in nodes_by_file.get(file_path, []):
                            if source_node['id'] in self.graph and node_id in self.graph:
                                edges.append((source_node['id'], node_id))
        
        # 4. Create edges based on file structure (files in same directory)
        files_by_dir = defaultdict(list)
        for file_path in nodes_by_file.keys():
            dir_path = '/'.join(file_path.split('/')[:-1]) if '/' in file_path else ''
            files_by_dir[dir_path].append(file_path)
        
        # Connect nodes in related files
        for dir_path, related_files in files_by_dir.items():
            if len(related_files) > 1:
                for i, file1 in enumerate(related_files):
                    for file2 in related_files[i+1:]:
                        nodes1 = nodes_by_file[file1]
                        nodes2 = nodes_by_file[file2]
                        # Connect first node of each file
                        if nodes1 and nodes2:
                            id1 = nodes1[0]['id']
                            id2 = nodes2[0]['id']
                            if id1 in self.graph and id2 in self.graph:
                                edges.append((id1, id2))
        
        # Add edges to graph (avoid duplicates)
        added_edges = set()
        for source, target in edges:
            edge_key = (source, target)
            if edge_key not in added_edges and source in self.graph and target in self.graph:
                self.graph.add_edge(source, target)
                added_edges.add(edge_key)
        
        # Analyze graph
        analysis = self._analyze_graph()
        
        return {
            "nodes": [
                {
                    "id": node_id,
                    **self.graph.nodes[node_id]
                }
                for node_id in self.graph.nodes()
            ],
            "edges": [
                {
                    "source": source,
                    "target": target,
                    "weight": self.graph[source][target].get('weight', 1)
                }
                for source, target in self.graph.edges()
            ],
            "analysis": analysis
        }
    
    def _analyze_graph(self) -> Dict:
        """Analyze graph for issues"""
        analysis = {
            "dead_functions": [],
            "circular_dependencies": [],
            "high_coupling": [],
            "hotspots": []
        }
        
        # Find dead functions (no incoming edges)
        for node_id in self.graph.nodes():
            if self.graph.in_degree(node_id) == 0 and self.graph.out_degree(node_id) == 0:
                node_data = self.graph.nodes[node_id]
                if node_data.get('type') == 'function':
                    analysis["dead_functions"].append(node_id)
        
        # Find circular dependencies
        try:
            cycles = list(nx.simple_cycles(self.graph))
            analysis["circular_dependencies"] = cycles[:10]  # Limit to first 10
        except:
            pass
        
        # Find high coupling (many connections)
        coupling_scores = {}
        for node_id in self.graph.nodes():
            coupling = self.graph.degree(node_id)
            coupling_scores[node_id] = coupling
        
        # Top 10 high coupling nodes
        high_coupling = sorted(coupling_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        analysis["high_coupling"] = [node_id for node_id, _ in high_coupling]
        
        # Find hotspots (many incoming calls)
        in_degrees = dict(self.graph.in_degree())
        hotspots = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:10]
        analysis["hotspots"] = [node_id for node_id, _ in hotspots]
        
        return analysis

