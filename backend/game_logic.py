from typing import Dict, List
import random


# Définition des personnages et leurs pouvoirs
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
        print(f"[LOG] Joueur créé : {self.nom} avec {self.or_} Or.")

    def ajouter_carte(self, carte: str):
        self.cartes.append(carte)
        print(f"[LOG] {self.nom} a reçu la carte {carte}.")

    def perdre_carte(self):
        """Le joueur perd une carte et la dévoile"""
        if self.cartes:
            carte_perdue = self.cartes.pop()
            print(f"[LOG] {self.nom} perd la carte {carte_perdue}.")
            return carte_perdue
        return None

    def afficher_info(self):
        print(f"{self.nom} - Or: {self.or_}, Cartes: {self.cartes}")

class Partie:
    def __init__(self, joueurs: List[str]):
        print("[LOG] Initialisation de la partie...")
        self.joueurs = {nom: Joueur(nom) for nom in joueurs}
        self.cour = self.initialiser_cartes()
        print("[LOG] Cartes mélangées et prêtes à être distribuées.")

    def initialiser_cartes(self) -> List[str]:
        """Mélange et distribue les cartes."""
        cartes = [p for p in PERSONNAGES.keys()] * 4  # 4 exemplaires de chaque personnage
        random.shuffle(cartes)
        return cartes

    def distribuer_cartes(self):
        """Donne 2 cartes à chaque joueur."""
        print("[LOG] Distribution des cartes...")
        for joueur in self.joueurs.values():
            joueur.ajouter_carte(self.cour.pop())
            joueur.ajouter_carte(self.cour.pop())
        print("[LOG] Cartes distribuées !")

    def afficher_etat(self):
        """Affiche l'état du jeu."""
        print("\n[LOG] État du jeu :")
        for joueur in self.joueurs.values():
            joueur.afficher_info()
        print("\n")

    def action_revenu(self, joueur: str):
        """Le joueur prend 1 Or du Trésor."""
        self.joueurs[joueur].or_ += 1
        print(f"[LOG] {joueur} prend 1 Or du Trésor.")

    def action_aide_etrangere(self, joueur: str):
        """Le joueur prend 2 Or du Trésor."""
        self.joueurs[joueur].or_ += 2
        print(f"[LOG] {joueur} prend 2 Or du Trésor.")

    def action_assassinat(self, attaquant: str, cible: str):
        """Assassiner un personnage adverse en dépensant 7 Or."""
        if self.joueurs[attaquant].or_ >= 7:
            self.joueurs[attaquant].or_ -= 7
            carte_perdue = self.joueurs[cible].perdre_carte()
            if carte_perdue:
                print(f"[LOG] {cible} perd la carte {carte_perdue} !")
            else:
                print(f"[LOG] {cible} est éliminé !")
        else:
            print("[LOG] Assassinat impossible, Or insuffisant.")

    def activation_pouvoir(self, joueur: str, personnage: str):
        """Le joueur utilise un pouvoir"""
        if personnage in self.joueurs[joueur].cartes:
            print(f"[LOG] {joueur} active le pouvoir de {personnage} !")
        else:
            print(f"[LOG] {joueur} bluffe en activant {personnage}...")

# Exemple de test
if __name__ == "__main__":
    print("[LOG] Démarrage du jeu Complots 2 Online...\n")
    
    partie = Partie(["Charles", "Alice", "Bob"])
    partie.distribuer_cartes()
    partie.afficher_etat()

    # Simulation d'actions
    partie.action_revenu("Charles")
    partie.action_aide_etrangere("Alice")
    partie.action_assassinat("Bob", "Alice")
    partie.activation_pouvoir("Charles", "Maître-Chanteur")

    partie.afficher_etat()

    print("\n[LOG] Fin du script. Tout semble fonctionner !")