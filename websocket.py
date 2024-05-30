import asyncio
import websockets

async def hello(websockets, path):
    bpm = await websockets.recv()
    print(f"< {bpm}!")
    seguro = f"estas bien"
    ayuda = f"estas mal"


    freq = int.from_bytes(bpm, "big")
    
    if freq > 180:

        await websockets.send(ayuda)

    else:

        await websockets.send(seguro)
    
    

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
