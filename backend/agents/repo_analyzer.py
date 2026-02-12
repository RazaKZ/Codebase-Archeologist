"""
Agent 1: Repo Analyzer
Clones repos and extracts AST (functions, classes, imports, dependencies)
"""
import os
import json
import tempfile
from pathlib import Path
from typing import Dict, List, Optional
from git import Repo
import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
import tree_sitter_typescript as tstypescript
from tree_sitter import Language, Parser

class RepoAnalyzer:
    def __init__(self):
        self.parsers = self._init_parsers()
    
    def _init_parsers(self) -> Dict[str, Parser]:
        """Initialize tree-sitter parsers for different languages"""
        parsers = {}
        
        # Python parser
        try:
            py_lang = Language(tspython.language())
            parsers['python'] = Parser(py_lang)
        except:
            pass
        
        # JavaScript parser
        try:
            js_lang = Language(tsjavascript.language())
            parsers['javascript'] = Parser(js_lang)
        except:
            pass
        
        # TypeScript parser
        try:
            ts_lang = Language(tstypescript.language())
            parsers['typescript'] = Parser(ts_lang)
        except:
            pass
        
        return parsers
    
    async def analyze_repo(self, repo_url: str, use_mcp: bool = False) -> Dict:
        """
        Analyze a repository and extract AST information
        
        Args:
            repo_url: GitHub repository URL
            use_mcp: Whether to use Repo Prompt MCP (if available)
        
        Returns:
            Dictionary with nodes and relationships
        """
        if use_mcp:
            # TODO: Integrate with Repo Prompt MCP
            pass
        
        # Clone repository to temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                repo = Repo.clone_from(repo_url, tmpdir)
                return await self._extract_ast(tmpdir)
            except Exception as e:
                # Fallback: analyze local directory if clone fails
                if os.path.exists(repo_url):
                    return await self._extract_ast(repo_url)
                raise Exception(f"Failed to clone repository: {str(e)}")
    
    async def _extract_ast(self, repo_path: str) -> Dict:
        """Extract AST from repository files"""
        nodes = []
        relationships = []
        imports_map = {}
        
        repo_path_obj = Path(repo_path)
        
        # Supported file extensions
        extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript'
        }
        
        for ext, lang in extensions.items():
            for file_path in repo_path_obj.rglob(f"*{ext}"):
                if any(skip in str(file_path) for skip in ['node_modules', '.git', 'venv', '__pycache__']):
                    continue
                
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    file_nodes, file_rels, file_imports = self._parse_file(
                        str(file_path.relative_to(repo_path_obj)),
                        content,
                        lang
                    )
                    nodes.extend(file_nodes)
                    relationships.extend(file_rels)
                    imports_map.update(file_imports)
                except Exception as e:
                    continue
        
        return {
            "nodes": nodes,
            "relationships": relationships,
            "imports": imports_map,
            "total_files": len(set(n['file'] for n in nodes)),
            "total_functions": len([n for n in nodes if n['type'] == 'function']),
            "total_classes": len([n for n in nodes if n['type'] == 'class'])
        }
    
    def _parse_file(self, file_path: str, content: str, language: str) -> tuple:
        """Parse a single file and extract AST nodes"""
        nodes = []
        relationships = []
        imports = {}
        
        if language not in self.parsers:
            return nodes, relationships, imports
        
        parser = self.parsers[language]
        tree = parser.parse(bytes(content, 'utf8'))
        
        # Extract functions, classes, and imports
        cursor = tree.walk()
        
        def traverse(node, depth=0):
            if depth > 20:  # Prevent infinite recursion
                return
            
            node_type = node.type
            
            if node_type == 'function_definition' or node_type == 'function_declaration':
                name = self._get_node_name(node, content)
                if name:
                    nodes.append({
                        "id": f"{file_path}::{name}",
                        "name": name,
                        "type": "function",
                        "file": file_path,
                        "line_start": node.start_point[0] + 1,
                        "line_end": node.end_point[0] + 1
                    })
            
            elif node_type == 'class_definition' or node_type == 'class_declaration':
                name = self._get_node_name(node, content)
                if name:
                    nodes.append({
                        "id": f"{file_path}::{name}",
                        "name": name,
                        "type": "class",
                        "file": file_path,
                        "line_start": node.start_point[0] + 1,
                        "line_end": node.end_point[0] + 1
                    })
            
            elif node_type == 'import_statement' or node_type == 'import_from_statement':
                import_name = self._extract_import(node, content)
                if import_name:
                    imports[file_path] = imports.get(file_path, []) + [import_name]
            
            # Traverse children
            if node.child_count > 0:
                cursor.goto_first_child()
                traverse(cursor.node, depth + 1)
                while cursor.goto_next_sibling():
                    traverse(cursor.node, depth + 1)
                cursor.goto_parent()
        
        traverse(tree.root_node)
        
        return nodes, relationships, imports
    
    def _get_node_name(self, node, content: str) -> Optional[str]:
        """Extract name from a node"""
        for child in node.children:
            if child.type == 'identifier' or child.type == 'type_identifier':
                start = child.start_byte
                end = child.end_byte
                return content[start:end]
        return None
    
    def _extract_import(self, node, content: str) -> Optional[str]:
        """Extract import name from import node"""
        for child in node.children:
            if child.type in ['dotted_name', 'identifier', 'string']:
                start = child.start_byte
                end = child.end_byte
                return content[start:end].strip('"\'')
        return None

