// Variable globale pour l'utilisateur courant
let currentUser = "";

// Appelée lors du clic sur le bouton "Rejoindre"
async function joinGame() {
  const pseudo = document.getElementById("player-name").value.trim();
  if (!pseudo) {
    alert("Veuillez entrer un pseudo !");
    return;
  }
  currentUser = pseudo;
  const response = await fetch(`https://complot-backend.onrender.com/game/join/${pseudo}`, {
    method: "POST"
  });
  const data = await response.json();
  console.log(data.message);
  // Masquer l'écran d'accueil et afficher l'écran de jeu
  document.getElementById("welcome-screen").classList.add("hidden");
  document.getElementById("game-screen").classList.remove("hidden");
  updatePlayersList();
  updateTurn();
}

// Lance la partie (doit être lancé par un joueur ou un modérateur)
async function startGame() {
  const response = await fetch("https://complot-backend.onrender.com/game/start", { method: "POST" });
  const data = await response.json();
  alert(data.message);
  updateTurn();
}

// Met à jour l'affichage des joueurs dans le cercle
async function updatePlayersList() {
  const response = await fetch("https://complot-backend.onrender.com/game/status");
  const data = await response.json();
  // data.joueurs est un tableau de pseudos, data.cartes est un objet {pseudo: [carte, carte]}
  data.joueurs.forEach((pseudo, index) => {
    // Met à jour le pseudo
    const playerBox = document.getElementById(`player-${index + 1}`);
    playerBox.querySelector(".player-name").textContent = pseudo;
    // Pour les cartes, si c'est l'utilisateur connecté, on affiche ses cartes ; sinon on affiche des masques
    const cardsDiv = document.getElementById(`cards-${index + 1}`);
    if (pseudo === currentUser) {
      cardsDiv.textContent = "Cartes : " + data.cartes[pseudo].join(" , ");
    } else {
      cardsDiv.textContent = "Cartes : ???";
    }
  });
}

// Met à jour l'affichage du joueur dont c'est le tour
async function updateTurn() {
  const response = await fetch("https://complot-backend.onrender.com/game/turn");
  const data = await response.json();
  const tourActuel = data.tour_actuel;
  document.getElementById("current-turn").textContent = tourActuel;
  
  // Affiche le popup d'action uniquement si c'est le tour de l'utilisateur connecté
  const popup = document.getElementById("action-popup");
  if (currentUser === tourActuel) {
    popup.classList.remove("hidden");
  } else {
    popup.classList.add("hidden");
  }
}

// Gère l'action réalisée par le joueur actif via le popup
async function playAction(action) {
  // Appeler l'endpoint d'action
  const turnResponse = await fetch("https://complot-backend.onrender.com/game/turn");
  const turnData = await turnResponse.json();
  const joueurActif = turnData.tour_actuel;
  
  // Vérifie que c'est bien le tour du joueur connecté (sécurité côté client)
  if (currentUser !== joueurActif) {
    alert("Ce n'est pas votre tour !");
    return;
  }
  
  await fetch(`https://complot-backend.onrender.com/game/action/${joueurActif}/${action}`, {
    method: "POST"
  });
  
  // Après l'action, on passe au tour suivant
  await fetch("https://complot-backend.onrender.com/game/next_turn", { method: "POST" });
  // Mise à jour de l'affichage
  updatePlayersList();
  updateTurn();
  // Ici, on pourrait aussi rafraîchir l'historique des actions si besoin
  fetchGameActions();
}

// (Optionnel) Fonction pour rafraîchir l'historique des actions
async function fetchGameActions() {
  const response = await fetch("https://complot-backend.onrender.com/game/status"); // Adapté selon l'endpoint d'actions
  const data = await response.json();
  // Mise à jour d'un élément avec l'historique (à implémenter)
  document.getElementById("actions-list").textContent = "Historique non implémenté pour le moment.";
}

// Rafraîchit périodiquement l'affichage (toutes les 5 secondes, par exemple)
setInterval(updatePlayersList, 5000);
setInterval(updateTurn, 5000);