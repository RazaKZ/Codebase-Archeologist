# Deployment Guide

## Local Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Docker Deployment

### Using Docker Compose
```bash
docker-compose up -d
```

This will start:
- Backend API on port 8000
- PostgreSQL database on port 5432

## Production Deployment

### Backend (Railway)

1. Create a Railway account at https://railway.app
2. Create a new project
3. Connect your GitHub repository
4. Add environment variables:
   - `DATABASE_URL` (Railway will auto-create PostgreSQL)
   - `GEMINI_API_KEY` (optional)
   - `SNYK_API_KEY` (optional)
   - `CORS_ORIGINS` (your frontend URL)
5. Deploy using the Dockerfile

### Frontend (Vercel)

1. Create a Vercel account at https://vercel.com
2. Import your GitHub repository
3. Configure:
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Add environment variable:
   - `VITE_API_URL` (your Railway backend URL)
5. Deploy

### Environment Variables

#### Backend (.env)
```
DATABASE_URL=postgresql://...
GEMINI_API_KEY=your_key_here
SNYK_API_KEY=your_key_here
CORS_ORIGINS=https://your-frontend.vercel.app
```

#### Frontend (.env)
```
VITE_API_URL=https://your-backend.railway.app
```

## Free Tier Limits

- **Railway**: 500 hours/month free
- **Vercel**: Unlimited for personal projects
- **Gemini API**: Free tier available
- **Snyk Code**: Free tier available

## Troubleshooting

### Backend won't start
- Check database connection string
- Verify all dependencies are installed
- Check logs: `docker-compose logs backend`

### Frontend can't connect to backend
- Verify CORS settings in backend
- Check API URL in frontend `.env`
- Ensure backend is running and accessible

