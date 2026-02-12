# 🚀 Live Deployment Guide - Codebase Archeologist

Complete step-by-step guide to deploy your project live!

---

## 📋 Prerequisites

Before starting, make sure you have:
- ✅ GitHub account (project should be on GitHub)
- ✅ Railway account (for backend) - https://railway.app
- ✅ Vercel account (for frontend) - https://vercel.com
- ✅ Google Gemini API Key (optional but recommended) - https://makersuite.google.com/app/apikey

---

## Part 1: Backend Deployment (Railway) 🚂

### Step 1: Prepare Backend for Deployment

1. **Check your backend structure:**
   ```bash
   cd backend
   ls
   ```
   Make sure you have:
   - `main.py`
   - `requirements.txt`
   - `Dockerfile` (or we'll create one)

2. **Create/Check Dockerfile** (if not exists):
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. **Update railway.json** (already exists, just verify):
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "DOCKERFILE",
       "dockerfilePath": "Dockerfile"
     },
     "deploy": {
       "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

### Step 2: Deploy to Railway

1. **Go to Railway:**
   - Visit https://railway.app
   - Sign up/Login with GitHub

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select the repository

3. **Configure Service:**
   - Railway will auto-detect it's a Python project
   - It will look for `Dockerfile` or `requirements.txt`
   - Make sure root directory is set to `backend/` (if needed)

4. **Add Environment Variables:**
   Click on your service → Variables tab → Add these:

   ```
   DATABASE_URL=sqlite:///./codebase_archeologist.db
   ```
   (Railway will auto-create PostgreSQL, but SQLite works too)

   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   (Get from: https://makersuite.google.com/app/apikey)

   ```
   CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173
   ```
   (We'll update this after frontend deployment)

   ```
   LLM_MODEL=gemini-1.5-flash
   ```

5. **Deploy:**
   - Railway will automatically start building
   - Wait for deployment to complete
   - Check logs if there are errors

6. **Get Your Backend URL:**
   - Go to Settings → Generate Domain
   - Copy the URL (e.g., `https://your-app.up.railway.app`)
   - **Save this URL!** You'll need it for frontend

### Step 3: Test Backend

1. **Check Health:**
   - Visit: `https://your-backend-url.up.railway.app/health`
   - Should return: `{"status": "healthy"}`

2. **Check API Docs:**
   - Visit: `https://your-backend-url.up.railway.app/docs`
   - Should show FastAPI Swagger UI

---

## Part 2: Frontend Deployment (Vercel) ⚡

### Step 1: Prepare Frontend

1. **Update vite.config.ts:**
   ```typescript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'

   export default defineConfig({
     plugins: [react()],
     server: {
       port: 5173,
       proxy: {
         '/api': {
           target: process.env.VITE_API_URL || 'http://localhost:8000',
           changeOrigin: true,
         },
         '/ws': {
           target: process.env.VITE_API_URL?.replace('http', 'ws') || 'ws://localhost:8000',
           ws: true,
         },
       },
     },
   })
   ```

2. **Create frontend/.env.production** (optional):
   ```
   VITE_API_URL=https://your-backend-url.up.railway.app
   ```

3. **Update API service** (if needed):
   Check `frontend/src/services/api.ts` - make sure it uses:
   ```typescript
   const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
   ```

### Step 2: Deploy to Vercel

1. **Go to Vercel:**
   - Visit https://vercel.com
   - Sign up/Login with GitHub

2. **Import Project:**
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Select the repository

3. **Configure Project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend` (IMPORTANT!)
   - **Build Command:** `npm run build` (auto-detected)
   - **Output Directory:** `dist` (auto-detected)
   - **Install Command:** `npm install` (auto-detected)

4. **Add Environment Variables:**
   Click "Environment Variables" → Add:
   ```
   VITE_API_URL = https://your-backend-url.up.railway.app
   ```
   (Use the Railway URL you saved earlier)

5. **Deploy:**
   - Click "Deploy"
   - Wait for build to complete
   - Vercel will give you a URL like: `https://your-app.vercel.app`

6. **Update vercel.json** (if needed):
   ```json
   {
     "buildCommand": "cd frontend && npm install && npm run build",
     "outputDirectory": "frontend/dist",
     "framework": "vite",
     "rewrites": [
       {
         "source": "/api/:path*",
         "destination": "https://your-backend-url.up.railway.app/api/:path*"
       },
       {
         "source": "/ws/:path*",
         "destination": "https://your-backend-url.up.railway.app/ws/:path*"
       }
     ]
   }
   ```

### Step 3: Update Backend CORS

1. **Go back to Railway:**
   - Open your backend service
   - Go to Variables
   - Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.vercel.app,http://localhost:5173
   ```
   (Replace with your actual Vercel URL)

2. **Redeploy Backend:**
   - Railway will auto-redeploy when you change variables
   - Or manually trigger: Settings → Redeploy

---

## Part 3: Final Configuration 🔧

### Step 1: Test Everything

1. **Test Frontend:**
   - Visit your Vercel URL
   - Try to analyze a repository
   - Check browser console (F12) for errors

2. **Test Backend Connection:**
   - Open browser console
   - Check Network tab
   - API calls should go to Railway URL

3. **Test WebSocket:**
   - Start an analysis
   - Should see real-time progress updates

### Step 2: Get Gemini API Key (Optional but Recommended)

1. **Visit:** https://makersuite.google.com/app/apikey
2. **Sign in** with Google account
3. **Create API Key**
4. **Copy the key**
5. **Add to Railway:**
   - Go to Railway → Your Service → Variables
   - Add: `GEMINI_API_KEY=your_key_here`
   - Redeploy

### Step 3: Custom Domain (Optional)

**Vercel:**
- Go to Project Settings → Domains
- Add your custom domain
- Follow DNS instructions

**Railway:**
- Go to Settings → Domains
- Add custom domain
- Update CORS_ORIGINS with new domain

---

## 🐛 Troubleshooting

### Backend Issues

**Problem: Backend won't start**
- Check Railway logs
- Verify `main.py` exists in backend folder
- Check if `requirements.txt` is correct
- Make sure Dockerfile is in backend/ directory

**Problem: Database errors**
- SQLite works by default
- For PostgreSQL, Railway auto-creates it
- Check DATABASE_URL in environment variables

**Problem: CORS errors**
- Update CORS_ORIGINS with your frontend URL
- Make sure URL has https:// (not http://)
- Redeploy backend after changing CORS

### Frontend Issues

**Problem: Can't connect to backend**
- Check VITE_API_URL in Vercel environment variables
- Verify backend URL is correct (with https://)
- Check browser console for errors
- Make sure CORS is configured in backend

**Problem: Build fails**
- Check Vercel build logs
- Make sure root directory is `frontend`
- Verify package.json exists
- Check for TypeScript errors

**Problem: WebSocket not working**
- Check if backend WebSocket endpoint is accessible
- Verify WebSocket URL in frontend code
- Check Railway logs for WebSocket errors

### Common Fixes

**Clear cache:**
```bash
# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# Backend
cd backend
rm -rf venv
python -m venv venv
pip install -r requirements.txt
```

**Check URLs:**
- Backend: `https://your-app.up.railway.app/health`
- Frontend: `https://your-app.vercel.app`
- API Docs: `https://your-app.up.railway.app/docs`

---

## ✅ Deployment Checklist

- [ ] Backend deployed on Railway
- [ ] Backend URL working (health check passes)
- [ ] Environment variables set in Railway
- [ ] Frontend deployed on Vercel
- [ ] Frontend URL working
- [ ] VITE_API_URL set in Vercel
- [ ] CORS_ORIGINS updated with frontend URL
- [ ] Gemini API key added (optional)
- [ ] Tested repository analysis
- [ ] WebSocket working (real-time updates)
- [ ] Chat assistant working (if API key added)

---

## 🎉 You're Live!

Your project is now deployed at:
- **Frontend:** https://your-app.vercel.app
- **Backend:** https://your-app.up.railway.app
- **API Docs:** https://your-app.up.railway.app/docs

**Share your project and enjoy! 🚀**

---

## 📞 Need Help?

If you face any issues:
1. Check Railway logs (Deployments → View Logs)
2. Check Vercel logs (Deployments → View Logs)
3. Check browser console (F12)
4. Verify all environment variables are set
5. Make sure both services are deployed successfully

---

## 💰 Free Tier Limits

**Railway:**
- 500 hours/month free
- $5 credit monthly
- Auto-sleeps after inactivity

**Vercel:**
- Unlimited deployments
- Free for personal projects
- 100GB bandwidth/month

**Gemini API:**
- Free tier available
- 15 requests per minute
- 1 million tokens per day

---

**Good luck with your deployment! 🎊**

