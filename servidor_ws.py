import asyncio
import websockets

clientes = set()

async def manejar_cliente(websocket):
    print(" Cliente conectado")
    clientes.add(websocket)
    try:
        async for mensaje in websocket:
            print(" Mensaje recibido:", mensaje)
            for cliente in clientes:
                await cliente.send(mensaje)
    except websockets.exceptions.ConnectionClosed:
        print(" Cliente desconectado inesperadamente")
    finally:
        clientes.remove(websocket)
        print(" Cliente desconectado")

async def iniciar_servidor():
    server = await websockets.serve(manejar_cliente, "localhost", 6790)
    print("Servidor WebSocket en ws://localhost:6790")
    await server.wait_closed()

asyncio.run(iniciar_servidor())
