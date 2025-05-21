from fastapi import FastAPI
from backend.game_logic import Partie

app = FastAPI()

# Initialiser une partie
partie = Partie(["Charles", "Alice", "Bob"])
partie.distribuer_cartes()

@app.get("/game/status")
def get_game_status():
    """Retourne l'état actuel du jeu"""
    joueurs_info = {j.nom: {"or": j.or_, "cartes": j.cartes} for j in partie.joueurs.values()}
    return {"joueurs": joueurs_info, "tresor": sum(j.or_ for j in partie.joueurs.values())}