import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"

def test_create_and_state():
    r = client.post("/game/create", json=["Alice","Bob"] )
    assert r.status_code == 200
    game_id = r.json()["game_id"]
    r2 = client.get(f"/game/{game_id}/state")
    assert r2.status_code == 200
    data = r2.json()
    assert data["turn"] in ["Alice","Bob"]