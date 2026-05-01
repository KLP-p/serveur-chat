import os
import asyncio
import websockets
from cryptography.fernet import Fernet

FERNET_KEY = b"r7eERj6U4XJtS0R8FPq-9odUIDnoRpi5SUvxwHU5Op8="
cipher = Fernet(FERNET_KEY)

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            # message = texte chiffré (Fernet base64 en str)
            # on le relaye tel quel
            dead = []
            for ws in clients:
                try:
                    await ws.send(message)
                except:
                    dead.append(ws)
            for ws in dead:
                clients.discard(ws)
    finally:
        clients.discard(websocket)

async def main():
    port = int(os.environ.get("PORT", 10000))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"WebSocket server listening on 0.0.0.0:{port}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
