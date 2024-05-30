import asyncio
import websockets


async def hello():
    url = "ws://localhost:8765"
    async with websockets.connect(url) as websocket:

        name = int (input("tu presion es:"))
        seguro = f"bien"
        ayuda = f"mal"

        if name > 180:

            await websocket.send(ayuda)
            
        else:

            await websocket.send(seguro)


        alerta = await websocket.recv()
        print(f"<{alerta}")



asyncio.get_event_loop().run_until_complete(hello())
