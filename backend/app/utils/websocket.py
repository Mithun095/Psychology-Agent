"""
WebSocket Manager
Manages WebSocket connections for real-time chat

Author: Vignesh (Backend Developer)
"""

from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        # Map user_id to list of WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept and store WebSocket connection"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        print(f"✅ WebSocket connected for user: {user_id}")
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove WebSocket connection"""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            
            # Remove user entry if no more connections
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        print(f"❌ WebSocket disconnected for user: {user_id}")
    
    async def send_personal_message(self, message: dict, user_id: str):
        """Send message to specific user's all connections"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for user_connections in self.active_connections.values():
            for connection in user_connections:
                await connection.send_json(message)
    
    def get_active_users_count(self) -> int:
        """Get number of active users"""
        return len(self.active_connections)


# Global connection manager instance
manager = ConnectionManager()


