Now create the CORE ANALYZER ENGINE:

Build a multi-agent system using LangGraph (Python) that:

AGENT 1: REPO ANALYZER
- Takes GitHub repo URL
- Clones locally or uses Repo Prompt MCP
- Extracts AST: functions, classes, imports, dependencies
- Output: JSON of all nodes and relationships

AGENT 2: DEPENDENCY MAPPER
- Takes AST output from Agent 1
- Builds Neo4j graph (or NetworkX fallback)
- Identifies:
  - Dead functions (no callers)
  - Circular dependencies
  - High-coupling modules
  - Hotspots (many incoming calls)
- Output: Graph nodes + edges with weights

AGENT 3: BUSINESS LOGIC EXTRACTOR
- Takes function/class clusters
- Uses Gemini API (via Code Wiki) or Snyk AI
- Reverse engineers intent:
  - "This function validates SSN numbers"
  - "This module handles payment processing"
- Adds confidence scores (0.0-1.0)
- Output: Annotated nodes with natural language descriptions

AGENT 4: IMPACT ANALYZER
- Takes user question: "What breaks if I delete X?"
- Traverses graph forward/backward
- Lists all affected components
- Risk rating: HIGH/MEDIUM/LOW
- Output: Markdown report + visual graph

AGENT 5: ORCHESTRATOR
- Manages state between agents
- Handles errors and retries
- Caches results to avoid redundant LLM calls
- Streams progress to frontend via WebSockets

Implementation:
1. Use LangGraph for stateful workflows
2. All agents must have fallback modes (no API dependency)
3. Add comprehensive error handling
4. Include confidence scoring for all AI outputs
5. Make it async and scalable