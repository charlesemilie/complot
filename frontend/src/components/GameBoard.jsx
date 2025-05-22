import React from 'react'
import PlayerHand from './PlayerHand'
import Chat from './Chat'

export default function GameBoard({ state, gameId }) { // REÇOIT gameId
  return (
    <div>
      <div className="grid grid-cols-2 gap-4">
        {state.players.map(p => <PlayerHand key={p.name} player={p} />)}
      </div>
      <Chat gameId={gameId} /> {/* PASSE gameId à Chat */}
    </div>
  )
}