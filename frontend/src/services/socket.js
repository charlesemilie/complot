export function connectSocket(gameId) {
  const url = `${process.env.REACT_APP_API_URL.replace(/^http/, 'ws')}/game/ws/${gameId}`
  return new WebSocket(url)
}