import os
import asyncio
import websockets
from websockets.http import Headers
from cryptography.fernet import Fernet

FERNET_KEY = b"r7eERj6U4XJtS0R8FPq-9odUIDnoRpi5SUvxwHU5Op8="
cipher = Fernet(FERNET_KEY)

clients = set()

# Réponse HTTP simple pour Railway (GET / HEAD)
async def http_handler(path, request_headers):
    upgrade = request_headers.get("Upgrade", "").lower()

    if upgrade != "websocket":
        return (
            200,
            Headers({"Content-Type": "text/plain"}),
            b"RedTiger WebSocket Server OK\n"
        )

async def ws_handler(websocket, path):
    print("Client WebSocket connecté !")
    clients.add(websocket)
    try:
        async for encrypted_msg in websocket:
            dead = []
            for ws in clients:
                try:
                    await ws.send(encrypted_msg)
                except:
                    dead.append(ws)
            for ws in dead:
                clients.discard(ws)
    finally:
        clients.discard(websocket)

async def main():
    port = int(os.environ.get("PORT", 8000))
    print(f"WebSocket server running on port {port}")

    async with websockets.serve(
        ws_handler,
        "0.0.0.0",
        port,
        process_request=http_handler
    ):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
