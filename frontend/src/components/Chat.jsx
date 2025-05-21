import React, { useState, useEffect } from 'react'
import { connectSocket } from '../services/socket'

export default function Chat() {
  const [msgs, setMsgs] = useState([])
  const [text, setText] = useState('')
  useEffect(() => {
    const socket = connectSocket('chat')
    socket.onmessage = e => setMsgs(msgs => [...msgs, JSON.parse(e.data)])
  }, [])

  const send = () => {
    // TODO: implémenter chat
  }

  return (
    <div className="mt-4">
      <h3 className="font-semibold mb-2">Chat</h3>
      <div className="h-40 overflow-auto border p-2">
        {msgs.map((m,i) => <p key={i}>{m}</p>)}
      </div>
      <input value={text} onChange={e=>setText(e.target.value)} />
      <button onClick={send}>Envoyer</button>
    </div>
  )
}