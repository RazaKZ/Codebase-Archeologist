"""
WebSocket connection manager for real-time updates
"""
from fastapi import WebSocket
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def send_to_client(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)
    
    async def send_progress(self, client_id: str, agent: str, progress: float, message: str):
        await self.send_to_client(client_id, {
            "type": "progress",
            "agent": agent,
            "progress": progress,
            "message": message
        })
    
    async def send_result(self, client_id: str, agent: str, result: dict):
        await self.send_to_client(client_id, {
            "type": "result",
            "agent": agent,
            "data": result
        })

