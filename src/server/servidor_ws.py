import asyncio
import websockets
import os

clientes = set()

async def manejar_cliente(websocket):
    print("🔌 Cliente conectado")
    clientes.add(websocket)
    try:
        async for mensaje in websocket:
            print("📩 Mensaje recibido:", mensaje)
            for cliente in clientes:
                await cliente.send(mensaje)
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ Cliente desconectado inesperadamente")
    finally:
        clientes.remove(websocket)
        print("👋 Cliente desconectado")

async def iniciar_servidor():
    puerto = os.getenv('PORT', 5000)
    server = await websockets.serve(manejar_cliente, "0.0.0.0", int(puerto))
    print(f"🚀 Servidor WebSocket en ws://0.0.0.0:{puerto}")
    await server.wait_closed()

asyncio.run(iniciar_servidor())