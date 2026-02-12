Create deployment configuration for hackathon:

1. DOCKER:
   - Dockerfile for frontend (nginx)
   - Dockerfile for backend (uvicorn)
   - docker-compose.yml with:
     - backend service
     - frontend service  
     - redis (celery broker)
     - postgres (optional)

2. RAILWAY/VERCEL DEPLOYMENT:
   - backend: Railway (free tier)
   - frontend: Vercel (free tier)
   - Add environment variables template (.env.example)

3. DEMO MODE FEATURE:
   - If no repo provided → load sample data
   - Sample: FastAPI or Flask repo pre-analyzed
   - One-click "Load Demo" button
   - All features work without API keys

4. FALLBACK CHAIN:
   Primary: Snyk Code API → Free (200 tests/month)
   Fallback 1: Repo Prompt MCP → 100% Free, local
   Fallback 2: AST parsing + NetworkX → 100% Free, no APIs
   Fallback 3: Pre-computed demo data → 100% reliable

5. PERFORMANCE OPTIMIZATION:
   - Response caching (Redis)
   - Lazy loading for large graphs
   - Web workers for heavy computation
   - Optimize React renders (useMemo, useCallback)

6. MONITORING:
   - Logging to files (debug mode)
   - Request timing headers
   - Error tracking endpoint