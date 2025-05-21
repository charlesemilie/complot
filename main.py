from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.game_logic import Partie

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://complot-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Liste des joueurs actifs et état de la partie
joueurs_actifs = []
tour_actuel = 0  # Indice du joueur actif
partie_en_cours = False  # La partie est-elle en cours ?
action_log = []  # Liste des actions jouées

# Initialiser une partie
partie = Partie(["Charles", "Alice", "Bob"])
partie.distribuer_cartes()

@app.post("/game/join/{pseudo}")
async def rejoindre_partie(pseudo: str):
    """Ajoute un joueur à la partie."""
    if pseudo not in joueurs_actifs:
        joueurs_actifs.append(pseudo)
    return {"message": f"{pseudo} a rejoint la partie", "joueurs": joueurs_actifs, "partie_en_cours": partie_en_cours}

@app.get("/game/players")
async def liste_joueurs():
    """Renvoie la liste des joueurs actifs avec leur index."""
    return {"joueurs": {index: pseudo for index, pseudo in enumerate(joueurs_actifs)}}

@app.post("/game/start")
async def lancer_partie():
    """Démarre la partie si au moins 2 joueurs sont présents."""
    global tour_actuel, partie_en_cours
    if len(joueurs_actifs) < 2:
        return {"message": "Il faut au moins 2 joueurs pour commencer la partie"}
    tour_actuel = 0  # Premier joueur commence
    partie_en_cours = True  # La partie commence
    return {"message": "La partie commence !", "joueur_actif": joueurs_actifs[tour_actuel], "partie_en_cours": partie_en_cours}

@app.get("/game/status")
async def get_game_status():
    """Retourne l'état actuel du jeu."""
    joueurs_info = {j.nom: {"or": j.or_, "cartes": j.cartes} for j in partie.joueurs.values()}
    return {"joueurs": joueurs_info, "tresor": sum(j.or_ for j in partie.joueurs.values()), "partie_en_cours": partie_en_cours}

@app.get("/game/turn")
async def tour_en_cours():
    """Renvoie le joueur dont c'est le tour."""
    return {"joueur_actif": joueurs_actifs[tour_actuel]}

@app.post("/game/next_turn")
async def prochain_tour():
    """Passe au joueur suivant."""
    global tour_actuel
    tour_actuel = (tour_actuel + 1) % len(joueurs_actifs)
    return {"message": f"Tour suivant : {joueurs_actifs[tour_actuel]}", "joueur_actif": joueurs_actifs[tour_actuel]}

@app.get("/game/actions")
async def get_game_actions():
    """Retourne l'historique des actions jouées."""
    return {"actions": action_log}

@app.post("/game/action/{joueur}/{action}")
async def execute_action(joueur: str, action: str):
    """Exécute une action et l'enregistre dans l'historique."""
    global action_log
    if joueur != joueurs_actifs[tour_actuel]:  # Vérifier si c'est bien son tour
        return {"message": "Ce n'est pas ton tour !"}

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

    await prochain_tour()  # Passe au joueur suivant
    return {"message": message, "joueur_actif": joueurs_actifs[tour_actuel]}