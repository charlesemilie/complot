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

async function fetchGameActions() {
    try {
        const response = await fetch("https://complot-backend.onrender.com/game/actions");
        const data = await response.json();

        console.log(data.actions); // Vérifier si les actions sont bien récupérées

        // Mettre à jour l'affichage des actions des joueurs
        const actionsDiv = document.getElementById("actions-list"); // Correction ici
        actionsDiv.innerHTML = ""; // Efface l'affichage précédent

        data.actions.forEach(action => {
            const actionElement = document.createElement("p");
            actionElement.textContent = action;
            actionsDiv.appendChild(actionElement);
        });
    } catch (error) {
        console.error("Erreur lors de la récupération des actions :", error);
    }
}

// Rafraîchir les actions toutes les 5 secondes
setInterval(fetchGameActions, 5000);
fetchGameActions(); // Exécuter une première fois au chargement

function playAction(joueur, action) {
    fetch(`https://complot-backend.onrender.com/game/action/${joueur}/${action}`, {
        method: "POST"
    }).then(response => response.json())
      .then(data => console.log(data.message))
      .catch(error => console.error("Erreur lors de l'exécution de l'action :", error));
}

async function joinGame() {
    const pseudo = document.getElementById("player-name").value;
    if (!pseudo) {
        alert("Veuillez entrer un pseudo !");
        return;
    }

    const response = await fetch(`https://complot-backend.onrender.com/game/join/${pseudo}`, {
        method: "POST",
    });
    const data = await response.json();
    console.log(data.message);

    document.getElementById("welcome-screen").style.display = "none";
    document.getElementById("game-screen").style.display = "block";
    updatePlayersList();
}

async function updatePlayersList() {
    const response = await fetch("https://complot-backend.onrender.com/game/players");
    const data = await response.json();
    
    const playersDiv = document.getElementById("players-list");
    playersDiv.innerHTML = "";
    data.joueurs.forEach(joueur => {
        const p = document.createElement("p");
        p.textContent = joueur;
        playersDiv.appendChild(p);
    });
}

// Rafraîchir la liste des joueurs toutes les 5 secondes
setInterval(updatePlayersList, 5000);