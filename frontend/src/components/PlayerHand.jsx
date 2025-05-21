import React from 'react'

export default function PlayerHand({ player }) {
  return (
    <div className="border rounded p-2">
      <h2 className="font-semibold">{player.name}</h2>
      <p>Pièces: {player.coins}</p>
      <p>Cartes: {player.hand_count}</p>
      <p>Statut: {player.alive ? 'En jeu' : 'Éliminé'}</p>
    </div>
  )
}