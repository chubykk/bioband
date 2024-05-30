import asyncio
import websockets


async def hello():
    url = "ws://localhost:8765"
    async with websockets.connect(url) as websocket:


        
        bpm = int (input("tu presion es:")).to_bytes(2, 'big')
        print (bpm)

    
        await websocket.send(bpm)
            

        alerta = await websocket.recv()
        print(f"<{alerta}")



asyncio.get_event_loop().run_until_complete(hello())
