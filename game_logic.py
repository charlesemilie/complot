from typing import Dict, List
import random

# Définition des personnages et pouvoirs
PERSONNAGES = {
    "Maître-Chanteur": "Prend 3 Or à un adversaire.",
    "Bourreau": "Assassine un personnage adverse.",
    "Ursuline": "Protège d’un assassinat.",
    "Illusionniste": "Échange une carte avec la Cour.",
    "Sorcière": "Contre un assassinat.",
    "Croque-Mort": "Récupère une carte d’un joueur éliminé.",
    "Pape": "Protège contre le vol.",
    "Justicier": "Vole 3 Or et redistribue au plus pauvre.",
    "Espion": "Regarde une carte adverse."
}

class Joueur:
    def __init__(self, nom: str):
        self.nom = nom
        self.or_ = 2  # Chaque joueur commence avec 2 Or
        self.cartes = []  # Cartes en main

    def ajouter_carte(self, carte: str):
        self.cartes.append(carte)

    def perdre_carte(self):
        if self.cartes:
            return self.cartes.pop()
        return None

class Partie:
    def __init__(self, joueurs: List[str]):
        self.joueurs = {nom: Joueur(nom) for nom in joueurs}
        self.cour = self.initialiser_cartes()

    def initialiser_cartes(self) -> List[str]:
        """Mélange et distribue les cartes."""
        cartes = [p for p in PERSONNAGES.keys()] * 4  # 4 exemplaires de chaque personnage
        random.shuffle(cartes)
        return cartes

    def distribuer_cartes(self):
        """Donne 2 cartes à chaque joueur."""
        for joueur in self.joueurs.values():
            joueur.ajouter_carte(self.cour.pop())
            joueur.ajouter_carte(self.cour.pop())

    def afficher_etat(self):
        """Affiche l'état du jeu."""
        for nom, joueur in self.joueurs.items():
            print(f"{nom} - Or: {joueur.or_}, Cartes: {joueur.cartes}")

# Exemple de test
if __name__ == "__main__":
    partie = Partie(["Charles", "Alice", "Bob"])
    partie.distribuer_cartes()
    partie.afficher_etat()