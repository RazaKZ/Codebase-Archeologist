"""
Codebase Archeologist - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os

from api.routes import analysis, projects, chat
from core.websocket_manager import ConnectionManager
from database.database import engine, Base
from config.settings import settings


# -----------------------------
# Database lifecycle
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


# -----------------------------
# App init
# -----------------------------
app = FastAPI(
    title="Codebase Archeologist API",
    description="Multi-agent codebase analysis system",
    version="1.0.0",
    lifespan=lifespan
)


# -----------------------------
# CORS CONFIG (LOCAL + PROD)
# -----------------------------
cors_origins = settings.CORS_ORIGINS

# Safety: ensure list
if isinstance(cors_origins, str):
    cors_origins = [
        origin.strip()
        for origin in cors_origins.split(",")
        if origin.strip()
    ]

print("✅ CORS ORIGINS:", cors_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,   # localhost + vercel
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, OPTIONS etc
    allow_headers=["*"],
    expose_headers=["*"],
)


# -----------------------------
# WebSocket manager
# -----------------------------
manager = ConnectionManager()


# -----------------------------
# Routers
# -----------------------------
app.include_router(
    analysis.router,
    prefix="/api/analysis",
    tags=["analysis"]
)

app.include_router(
    projects.router,
    prefix="/api/projects",
    tags=["projects"]
)

app.include_router(
    chat.router,
    prefix="/api",
    tags=["chat"]
)


# -----------------------------
# Basic routes
# -----------------------------
@app.get("/")
async def root():
    return {
        "message": "Codebase Archeologist API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/debug/cors")
async def debug_cors():
    return {
        "cors_origins": cors_origins,
        "type": type(cors_origins).__name__
    }


# -----------------------------
# WebSocket endpoint
# -----------------------------
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(
                f"Echo: {data}",
                websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)


# -----------------------------
# Local run
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
