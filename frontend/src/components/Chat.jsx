import React, { useState, useEffect } from 'react'
import { connectSocket } from '../services/socket'

export default function Chat({ gameId }) { // REÇOIT gameId
  const [msgs, setMsgs] = useState([])
  const [text, setText] = useState('')
  const [socket, setSocket] = useState(null); // Pour stocker la socket

  useEffect(() => {
    const newSocket = connectSocket(gameId) // UTILISE gameId
    newSocket.onmessage = e => setMsgs(msgs => [...msgs, JSON.parse(e.data)])
    setSocket(newSocket); // Stocke la socket

    return () => { // Fonction de nettoyage
      if (newSocket.readyState === WebSocket.OPEN) {
        newSocket.close();
      }
    };
  }, [gameId]) // Reconnecte si gameId change

  const send = () => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ type: 'chat', message: text, game_id: gameId })); // ENVOIE LE MESSAGE AVEC game_id
      setText('');
    }
  }

  return (
    <div className="mt-4">
      <h3 className="font-semibold mb-2">Chat</h3>
      <div className="h-40 overflow-auto border p-2">
        {msgs.map((m,i) => <p key={i}>{m.message}</p>)} {/* Affiche le contenu du message */}
      </div>
      <input value={text} onChange={e=>setText(e.target.value)} />
      <button onClick={send}>Envoyer</button>
    </div>
  )
}