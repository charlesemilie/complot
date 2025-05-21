from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuration CORS pour autoriser le frontend à appeler le backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://complot-frontend.onrender.com"],  # Autorise uniquement ton frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Liste des joueurs actifs
joueurs_actifs = []

@app.post("/game/join/{pseudo}")
async def rejoindre_partie(pseudo: str):
    if pseudo not in joueurs_actifs:
        joueurs_actifs.append(pseudo)
    return {"message": f"{pseudo} a rejoint la partie", "joueurs": joueurs_actifs}

@app.get("/game/players")
async def liste_joueurs():
    return {"joueurs": joueurs_actifs}


from backend.game_logic import Partie

action_log = []  # Liste des actions jouées


# Initialiser une partie
partie = Partie(["Charles", "Alice", "Bob"])
partie.distribuer_cartes()

@app.get("/game/status")
def get_game_status():
    """Retourne l'état actuel du jeu"""
    joueurs_info = {j.nom: {"or": j.or_, "cartes": j.cartes} for j in partie.joueurs.values()}
    return {"joueurs": joueurs_info, "tresor": sum(j.or_ for j in partie.joueurs.values())}

@app.get("/game/actions")
def get_game_actions():
    """Retourne l'historique des actions jouées"""
    return {"actions": action_log}

@app.post("/game/action/{joueur}/{action}")
def execute_action(joueur: str, action: str):
    """Exécute une action et l'enregistre dans l'historique"""
    global action_log  # On s'assure que la variable action_log est accessible
    message = f"{joueur} a joué l’action {action}"
    action_log.append(message)

    if action == "revenu":
        partie.action_revenu(joueur)
    elif action == "aide_etrangere":
        partie.action_aide_etrangere(joueur)
    elif action == "assassinat":
        return {"message": "Assassinat nécessite une cible"}
    elif action == "pouvoir":
        return {"message": "Activation de pouvoir nécessite un personnage"}
    else:
        return {"message": "Action inconnue"}

    return {"message": message}