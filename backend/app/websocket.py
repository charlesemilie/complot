from fastapi import WebSocket
from typing import Dict, List

# Simple manager
class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}

    async def connect(self, game_id: str, ws: WebSocket):
        await ws.accept()
        self.active.setdefault(game_id, []).append(ws)

    def disconnect(self, game_id: str, ws: WebSocket):
        self.active[game_id].remove(ws)

    async def broadcast(self, game_id: str, message: dict):
        for ws in self.active.get(game_id, []):
            await ws.send_json(message)

manager = ConnectionManager()