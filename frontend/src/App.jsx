import React, { useEffect, useState } from 'react'
import { connectSocket } from './services/socket'
import GameBoard from './components/GameBoard' // Vérifie le chemin

export default function App() {
  const [state, setState] = useState(null)
  const gameId = window.location.pathname.split('/').pop() || 'demo' // Récupère gameId ici

  useEffect(() => {
    const socket = connectSocket(gameId) // Utilise gameId ici
    socket.onmessage = e => setState(JSON.parse(e.data))
    // Ajoute un nettoyage pour la socket si tu recharges souvent le composant
    return () => socket.close();
  }, [gameId]) // Déclenche l'effet si gameId change

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Complot en ligne</h1>
      {state ? <GameBoard state={state} gameId={gameId} /> : <p>Chargement...</p>} {/* PASSE gameId à GameBoard */}
    </div>
  )
}