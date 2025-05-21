const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:10000'
export async function fetchState(gameId) {
  const res = await fetch(`${API_URL}/game/${gameId}/state`)
  return res.json()
}