import asyncio
import websockets

async def hello(websockets, path):
    name = await websockets.recv()
    print(f"< {name}!")
    seguro = f"bien"
    ayuda = f"mal"
    
    
    if name == ayuda:
        alerta = f"tu presion es mayor a 180!, vamos a inyectar medicamento"

        await websockets.send(alerta)
        print(f"> {alerta}")
    
    elif name == seguro:
        
        aviso = f"estas bien"
        await websockets.send(aviso)
        print(f">{aviso}")

    else:
        nada = f"no hay informacion"
        await websockets.send(nada)
        print(f">{nada}")

        

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
