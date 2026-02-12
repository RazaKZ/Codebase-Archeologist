# Project Structure

```
hackathon/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── repo_analyzer.py          # Agent 1: AST extraction
│   │   ├── dependency_mapper.py      # Agent 2: Graph building
│   │   ├── business_logic_extractor.py # Agent 3: AI-powered understanding
│   │   ├── impact_analyzer.py        # Agent 4: Impact prediction
│   │   └── orchestrator.py           # Agent 5: Workflow management
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── analysis.py           # Analysis endpoints
│   │       └── projects.py           # Project management
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py                # Configuration
│   ├── core/
│   │   ├── __init__.py
│   │   └── websocket_manager.py      # WebSocket handling
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py               # DB connection
│   │   └── models.py                  # SQLAlchemy models
│   ├── main.py                       # FastAPI app entry
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Backend Docker config
│   └── env.example                   # Environment template
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnalysisPanel.tsx     # Analysis input
│   │   │   ├── Dashboard.tsx         # Main dashboard
│   │   │   └── GraphVisualization.tsx # React Flow graph
│   │   ├── services/
│   │   │   └── api.ts                # API client
│   │   ├── store/
│   │   │   └── analysisStore.ts      # Zustand state
│   │   ├── App.tsx                   # Main app component
│   │   ├── main.tsx                  # Entry point
│   │   └── index.css                 # Global styles
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── prompts/                          # Original requirements
├── docker-compose.yml                # Local development
├── Dockerfile                        # Root Dockerfile
├── railway.json                      # Railway config
├── vercel.json                       # Vercel config
├── README.md                         # Main documentation
├── DEPLOYMENT.md                     # Deployment guide
├── HACKATHON_PITCH.md                # Pitch materials
├── EXECUTION_CHECKLIST.md            # 48-hour checklist
├── PROJECT_STRUCTURE.md              # This file
└── LICENSE                           # MIT License
```

## Key Components

### Backend Agents
- **Repo Analyzer**: Uses tree-sitter to parse code and extract AST
- **Dependency Mapper**: Builds NetworkX graph, finds issues
- **Business Logic Extractor**: Uses Gemini API to understand code
- **Impact Analyzer**: Traverses graph to predict impact
- **Orchestrator**: Manages workflow and streams progress

### Frontend Components
- **AnalysisPanel**: Input form for repository URL
- **Dashboard**: Shows progress and summary statistics
- **GraphVisualization**: Interactive React Flow dependency graph

### Data Flow
1. User submits repo URL → Frontend
2. Frontend → Backend API `/api/analysis/start`
3. Backend starts background task → Orchestrator
4. Orchestrator runs agents sequentially
5. Progress updates via WebSocket → Frontend
6. Results saved to database
7. Frontend displays graph and insights

## Technology Choices

- **FastAPI**: Modern, fast Python web framework
- **React Flow**: Best-in-class graph visualization
- **Zustand**: Lightweight state management
- **NetworkX**: Powerful graph analysis
- **Tree-sitter**: Fast, incremental parsing
- **LangGraph**: (Future) Agent orchestration framework

