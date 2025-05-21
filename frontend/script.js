async function fetchGameStatus() {
    try {
        const response = await fetch("https://complot-backend.onrender.com/game/status");
        const data = await response.json();

        // Mettre à jour l'affichage des joueurs
        const playersDiv = document.getElementById("players");
        playersDiv.innerHTML = ""; // Effacer l'affichage précédent

        Object.entries(data.joueurs).forEach(([nom, info]) => {
            const playerInfo = document.createElement("p");
            playerInfo.textContent = `${nom} - Or: ${info.or}, Cartes: ${info.cartes.join(", ")}`;
            playersDiv.appendChild(playerInfo);
        });

        // Mettre à jour le trésor
        document.getElementById("treasury").textContent = data.tresor;
    } catch (error) {
        console.error("Erreur lors de la récupération du statut du jeu :", error);
    }
}

// Rafraîchir l’état du jeu toutes les 5 secondes
setInterval(fetchGameStatus, 5000);
fetchGameStatus(); // Exécuter une première fois au chargement