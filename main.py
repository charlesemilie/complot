import random
from fastapi import FastAPI

app = FastAPI()

# Variables globales
joueurs_actifs = []          # liste des pseudos dans l'ordre de join
tour_actuel = 0              # indice du joueur dont c'est le tour
partie_en_cours = False
cartes_par_joueur = {}       # dictionnaire {pseudo: [carte1, carte2]}
cartes_disponibles = ["Duchesse", "Assassin", "Comtesse", "Capitaine", "Ambassadeur"]

@app.post("/game/join/{pseudo}")
async def rejoindre_partie(pseudo: str):
    """
    Chaque joueur rejoint la partie avec son pseudo. On lui attribue alors 2 cartes aléatoires.
    """
    if pseudo not in joueurs_actifs:
        joueurs_actifs.append(pseudo)
        # Distribuer 2 cartes aléatoires parmi les cartes disponibles
        cartes_par_joueur[pseudo] = random.sample(cartes_disponibles, 2)
    return {"message": f"{pseudo} a rejoint la partie", "joueurs": joueurs_actifs}

@app.get("/game/status")
async def statut_partie():
    """
    Retourne l'état de la partie : la liste des joueurs, les cartes attribuées et le joueur dont c'est le tour.
    Remarque : pour la sécurité, le client devra filtrer et n’afficher que ses propres cartes.
    """
    joueur_tour = joueurs_actifs[tour_actuel] if joueurs_actifs else None
    return {"joueurs": joueurs_actifs, "cartes": cartes_par_joueur, "tour_actuel": joueur_tour}

@app.post("/game/start")
async def lancer_partie():
    """
    Démarre la partie (nécessite au moins 2 joueurs) et fixe le premier tour.
    """
    global partie_en_cours, tour_actuel
    if len(joueurs_actifs) < 2:
        return {"message": "Il faut au moins 2 joueurs pour commencer"}
    partie_en_cours = True
    tour_actuel = 0
    return {"message": "La partie commence !", "tour_actuel": joueurs_actifs[tour_actuel]}

@app.get("/game/turn")
async def get_turn():
    """
    Retourne le pseudo du joueur dont c'est le tour.
    """
    joueur_tour = joueurs_actifs[tour_actuel] if joueurs_actifs else None
    return {"tour_actuel": joueur_tour}

@app.post("/game/next_turn")
async def prochain_tour():
    """
    Passe au joueur suivant et retourne le nouveau joueur actif.
    """
    global tour_actuel
    if joueurs_actifs:
        tour_actuel = (tour_actuel + 1) % len(joueurs_actifs)
    return {"message": f"Tour suivant : {joueurs_actifs[tour_actuel]}", "tour_actuel": joueurs_actifs[tour_actuel]}

@app.post("/game/action/{joueur}/{action}")
async def execute_action(joueur: str, action: str):
    """
    Exécute l'action demandée par le joueur.
    Pour l’instant, on ne modifie pas d'état de jeu réel.
    On renvoie simplement un message de confirmation.
    """
    # Ici, dans une implémentation complète, on vérifierait que c'est bien le tour du joueur
    # et on appliquerait les conséquences de l'action.
    return {"message": f"{joueur} a effectué l'action '{action}'"}