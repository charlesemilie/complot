import React, { useEffect, useState } from 'react'
import { connectSocket } from './services/socket'
import GameBoard from './components/GameBoard'

export default function App() {
  const [state, setState] = useState(null)
  useEffect(() => {
    const gameId = window.location.pathname.split('/').pop() || 'demo'
    const socket = connectSocket(gameId)
    socket.onmessage = e => setState(JSON.parse(e.data))
  }, [])

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Complot en ligne</h1>
      {state ? <GameBoard state={state} /> : <p>Chargement...</p>}
    </div>
  )
}