from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import PlayerDB, PlayerCreate, Player
from .game_logic import Game
from .websocket import manager
import uuid
from typing import List

router = APIRouter(prefix="/game")

# In-memory store de parties
games = {}

@router.post("/create")
def create_game(names: List[str]):
    game_id = str(uuid.uuid4())
    game = Game(names)
    game.start()
    games[game_id] = game
    return {"game_id": game_id, "players": names}

@router.get("/{game_id}/state")
def get_state(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(404, "Partie non trouvée")
    return {"players": [{"name": p.name, "coins": p.coins, "hand_count": len(p.hand), "alive": p.alive} for p in game.players], "turn": game.current_player().name}

@router.post("/{game_id}/action")
def action(game_id: str, action: dict):
    game = games.get(game_id)
    if not game:
        raise HTTPException(404, "Partie non trouvée")
    # Simplifié: parsage minimal
    act = action.get("type")
    if act == "income":
        game.income()
    elif act == "foreign_aid":
        game.foreign_aid()
    elif act == "coup":
        game.coup(action.get("target"))
    else:
        raise HTTPException(400, "Action inconnue")
    return {"status": "ok"}

@router.websocket("/ws/{game_id}")
async def ws_endpoint(websocket: WebSocket, game_id: str):
    await manager.connect(game_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # difuseur aux autres
            await manager.broadcast(game_id, {"event": "update"})
    except WebSocketDisconnect:
        manager.disconnect(game_id, websocket)