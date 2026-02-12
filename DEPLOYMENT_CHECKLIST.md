# ✅ Deployment Checklist

Quick checklist to deploy your project live!

## Before Starting

- [ ] Project is pushed to GitHub
- [ ] All code is committed
- [ ] You have Railway account (https://railway.app)
- [ ] You have Vercel account (https://vercel.com)
- [ ] You have Gemini API key (optional: https://makersuite.google.com/app/apikey)

---

## Backend Deployment (Railway)

### Setup
- [ ] Go to https://railway.app and login
- [ ] Click "New Project" → "Deploy from GitHub repo"
- [ ] Select your repository
- [ ] Railway will auto-detect Python project

### Configuration
- [ ] Set root directory to `backend/` (if needed)
- [ ] Add environment variable: `DATABASE_URL=sqlite:///./codebase_archeologist.db`
- [ ] Add environment variable: `GEMINI_API_KEY=your_key_here` (optional)
- [ ] Add environment variable: `LLM_MODEL=gemini-1.5-flash`
- [ ] Add environment variable: `CORS_ORIGINS=http://localhost:5173` (we'll update later)

### Deploy
- [ ] Wait for build to complete
- [ ] Check deployment logs for errors
- [ ] Generate domain in Railway settings
- [ ] Copy backend URL (e.g., `https://your-app.up.railway.app`)
- [ ] Test: Visit `https://your-backend-url/health` (should return `{"status": "healthy"}`)

---

## Frontend Deployment (Vercel)

### Setup
- [ ] Go to https://vercel.com and login
- [ ] Click "Add New..." → "Project"
- [ ] Import your GitHub repository

### Configuration
- [ ] Framework Preset: **Vite**
- [ ] Root Directory: **`frontend`** (IMPORTANT!)
- [ ] Build Command: `npm run build` (auto-detected)
- [ ] Output Directory: `dist` (auto-detected)
- [ ] Add environment variable: `VITE_API_URL=https://your-backend-url.up.railway.app`

### Deploy
- [ ] Click "Deploy"
- [ ] Wait for build to complete
- [ ] Copy frontend URL (e.g., `https://your-app.vercel.app`)

---

## Final Configuration

### Update Backend CORS
- [ ] Go back to Railway
- [ ] Update `CORS_ORIGINS` environment variable:
  ```
  https://your-frontend.vercel.app,http://localhost:5173
  ```
- [ ] Redeploy backend (or wait for auto-redeploy)

### Test Everything
- [ ] Visit your Vercel frontend URL
- [ ] Open browser console (F12)
- [ ] Try to analyze a repository
- [ ] Check for errors in console
- [ ] Verify API calls go to Railway backend
- [ ] Test WebSocket connection (should see real-time updates)

---

## Optional: Custom Domains

### Vercel Custom Domain
- [ ] Go to Vercel project → Settings → Domains
- [ ] Add your custom domain
- [ ] Update DNS as instructed
- [ ] Update `CORS_ORIGINS` in Railway with new domain

### Railway Custom Domain
- [ ] Go to Railway service → Settings → Domains
- [ ] Add custom domain
- [ ] Update `CORS_ORIGINS` with new domain

---

## Troubleshooting

### Backend Issues
- [ ] Check Railway logs
- [ ] Verify `main.py` exists
- [ ] Check `requirements.txt` is correct
- [ ] Verify Dockerfile is in `backend/` directory

### Frontend Issues
- [ ] Check Vercel build logs
- [ ] Verify `VITE_API_URL` is set correctly
- [ ] Check browser console for errors
- [ ] Verify CORS is configured in backend

### Connection Issues
- [ ] Backend URL accessible? (test `/health` endpoint)
- [ ] CORS_ORIGINS includes frontend URL?
- [ ] Environment variables set correctly?
- [ ] Both services deployed successfully?

---

## 🎉 Success!

Your project is live at:
- **Frontend:** https://your-app.vercel.app
- **Backend:** https://your-app.up.railway.app
- **API Docs:** https://your-app.up.railway.app/docs

**Share and enjoy! 🚀**

