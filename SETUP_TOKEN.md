# Quick Setup: Auth Token Add Karein

## ✅ Aapka Auth Token
```
45e0b45d-b9bb-4381-a57f-d50586900110
```

## 📝 Steps

### Windows PowerShell:
```powershell
cd backend

# .env file banayein
@"
# API Keys
SNYK_API_KEY=45e0b45d-b9bb-4381-a57f-d50586900110
GEMINI_API_KEY=

# Database
DATABASE_URL=sqlite:///./codebase_archeologist.db

# CORS Origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Analysis Settings
MAX_REPO_SIZE_MB=100
ANALYSIS_TIMEOUT_SECONDS=300
CACHE_TTL_SECONDS=3600

# LLM Settings
LLM_MODEL=gemini-pro
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=2000
"@ | Out-File -FilePath .env -Encoding utf8
```

### Ya Manually:
1. `backend` folder mein jayein
2. `env.example` file ko copy karein aur `.env` naam dein
3. `.env` file khol kar yeh line update karein:
   ```
   SNYK_API_KEY=45e0b45d-b9bb-4381-a57f-d50586900110
   ```

## ✅ Verify
```powershell
# Check karein ke file ban gayi
cd backend
cat .env
```

## 🚀 Ab Backend Start Karein
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Note**: Auth Token ko API key ki tarah use kar sakte hain - dono same tarah kaam karte hain!

