# Quick Start Guide

Get Codebase Archeologist running in 5 minutes!

## Prerequisites

- Python 3.11+
- Node.js 18+
- Git

## Step 1: Backend Setup

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
# Edit .env and add your API keys if you have them

# Start the server
uvicorn main:app --reload
```

Backend should now be running at http://localhost:8000

## Step 2: Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend should now be running at http://localhost:5173

## Step 3: Test It!

1. Open http://localhost:5173 in your browser
2. Enter a GitHub repository URL (e.g., `https://github.com/facebook/react`)
3. Click "Analyze Repository"
4. Watch the magic happen! ✨

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

**Missing dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Database errors:**
- The app uses SQLite by default, which should work out of the box
- If you see errors, delete `codebase_archeologist.db` and restart

### Frontend Issues

**Port 5173 already in use:**
- Vite will automatically use the next available port
- Check the terminal output for the actual URL

**Can't connect to backend:**
- Make sure backend is running on port 8000
- Check `vite.config.ts` proxy settings
- Verify CORS settings in backend

**Module not found errors:**
```bash
rm -rf node_modules package-lock.json
npm install
```

## Using Docker (Alternative)

If you prefer Docker:

```bash
# Start everything with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

## Next Steps

- Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Check [EXECUTION_CHECKLIST.md](EXECUTION_CHECKLIST.md) for hackathon prep
- Review [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) to understand the codebase

## Need Help?

- Check the [README.md](README.md) for more details
- Review error messages in browser console (F12) and terminal
- Ensure all dependencies are installed correctly

Happy analyzing! 🚀

