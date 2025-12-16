from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

router = APIRouter(prefix="/ws", tags=["Real-Time"])

# Store connected WebSockets
active_connections = set()


async def broadcast(message: str):
    """Send message to all active clients."""
    for connection in list(active_connections):
        try:
            await connection.send_text(message)
        except Exception:
            active_connections.remove(connection)


@router.websocket("/updates")
async def websocket_updates(ws: WebSocket):
    """
    WebSocket endpoint for real-time dashboard updates.
    Clients will receive:
      - connection confirmation
      - broadcasted updates
      - echo messages (for testing)
    """
    await ws.accept()
    active_connections.add(ws)

    await ws.send_text("🔌 Real-time connection established.")

    try:
        while True:
            # Wait for message from client
            msg = await ws.receive_text()

            # Echo back to sender
            await ws.send_text(f"Echo: {msg}")

            # Broadcast to all clients
            await broadcast(f"📡 Broadcast: {msg}")

    except WebSocketDisconnect:
        active_connections.remove(ws)
        await broadcast("⚠️ A user disconnected.")


# Optional background heartbeat (for dashboards)
async def heartbeat():
    """
    Sends a heartbeat message every 30 seconds.
    """
    while True:
        await broadcast("💓 Heartbeat: server alive")
        await asyncio.sleep(30)