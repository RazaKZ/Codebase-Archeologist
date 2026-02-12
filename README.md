# Codebase Archeologist 🏛️

A powerful multi-agent AI system that analyzes codebases, maps dependencies, extracts business logic, and provides impact analysis. Built for hackathon excellence.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![React](https://img.shields.io/badge/react-18.2.0-blue.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.2.2-blue.svg)

## 🎯 Overview

Codebase Archeologist is a comprehensive tool that helps developers understand complex codebases quickly. It uses a multi-agent AI system to analyze repositories, visualize dependencies, and predict the impact of code changes.

## ✨ Features

- **🤖 Multi-Agent Analysis**: 5 specialized AI agents working together
  - Repo Analyzer: Extracts AST and code structure
  - Dependency Mapper: Builds dependency graphs
  - Business Logic Extractor: AI-powered code understanding
  - Impact Analyzer: Predicts consequences of changes
  - Orchestrator: Manages workflow and streams progress

- **📊 Interactive Visualization**: React Flow-based dependency graphs
  - Real-time graph updates
  - Interactive node exploration
  - Zoom, pan, and mini-map
  - Color-coded risk indicators

- **🧠 AI-Powered Insights**: 
  - Natural language code descriptions
  - Confidence scores for reliability
  - Context-aware chat assistant
  - Uses Google Gemini 1.5 Flash

- **⚡ Real-time Progress**: WebSocket streaming of analysis progress
- **🔍 Impact Analysis**: See what breaks before you delete code
- **🎨 Modern UI**: Beautiful, responsive interface built with Tailwind CSS

## 🛠️ Tech Stack

### Frontend
- **React 18.2.0** - UI framework
- **TypeScript 5.2.2** - Type-safe development
- **Vite 5.0.8** - Build tool
- **Tailwind CSS 3.3.6** - Styling
- **React Flow 11.10.1** - Graph visualization
- **Zustand 4.4.7** - State management
- **Axios 1.6.2** - HTTP client

### Backend
- **FastAPI 0.104.1** - Web framework
- **Python 3.11** - Programming language
- **Uvicorn 0.24.0** - ASGI server
- **NetworkX 3.2.1** - Graph algorithms
- **Tree-sitter** - AST parsing (Python, JS, TS)
- **SQLAlchemy 2.0.23** - ORM
- **WebSockets 12.0** - Real-time communication

### AI & APIs
- **Google Gemini 1.5 Flash** - AI model for code understanding
- **Snyk Code API** - Security analysis (optional)

### Deployment
- **Vercel** - Frontend hosting
- **Railway** - Backend hosting

## 📦 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Set up environment variables
cp env.example .env
# Edit .env and add your API keys

# Start the server
uvicorn main:app --reload
```

Backend will run at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at `http://localhost:5173`

### Test It!

1. Open `http://localhost:5173` in your browser
2. Enter a GitHub repository URL (e.g., `https://github.com/facebook/react`)
3. Click "Analyze Repository"
4. Watch the magic happen! ✨

## 🚀 Deployment

### Quick Deployment Guide

See [LIVE_DEPLOYMENT_GUIDE.md](LIVE_DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

**Quick Steps:**
1. Deploy backend to Railway
2. Deploy frontend to Vercel
3. Configure environment variables
4. Update CORS settings

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=sqlite:///./codebase_archeologist.db
GEMINI_API_KEY=your_gemini_api_key_here
SNYK_API_KEY=your_snyk_key_here
CORS_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app
LLM_MODEL=gemini-1.5-flash
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
# For production: VITE_API_URL=https://your-backend.railway.app
```

## 🏗️ Architecture

### Multi-Agent System

1. **Repo Analyzer**: Clones repos and extracts AST
2. **Dependency Mapper**: Builds dependency graphs using NetworkX
3. **Business Logic Extractor**: AI-powered code understanding
4. **Impact Analyzer**: Predicts consequences of changes
5. **Orchestrator**: Manages agent workflows and streams progress

### System Flow

```
User Input → Frontend → FastAPI Backend → Agent System
                                      ↓
                              Database (SQLite/PostgreSQL)
                                      ↓
                              WebSocket → Real-time Updates
```

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- [Deployment Guide](LIVE_DEPLOYMENT_GUIDE.md) - Deploy to production
- [Features Overview](FEATURES.md) - Detailed feature list
- [Project Structure](PROJECT_STRUCTURE.md) - Codebase organization
- [API Keys Setup](API_KEYS_SETUP.md) - Configure API keys
- [Presentation](PRESENTATION.md) - Project presentation

## 🧪 Development

### Running Tests

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### Project Structure

```
hackathon/
├── backend/              # FastAPI backend
│   ├── agents/          # Multi-agent system
│   ├── api/             # API routes
│   ├── config/          # Configuration
│   ├── database/        # Database models
│   └── main.py          # Entry point
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   └── store/       # State management
│   └── package.json
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- React Flow for graph visualization
- FastAPI for the excellent web framework
- All the open-source libraries that made this possible

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for hackathon excellence**
