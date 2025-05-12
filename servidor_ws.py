
import asyncio
import os
import websockets

clientes = {}  # Diccionario para asociar websockets con nombres de usuario

async def manejar_cliente(websocket):
    try:
        nombre = await websocket.recv()  # Espera recibir el nombre de usuario
        clientes[websocket] = nombre
        print(f" {nombre} se ha conectado")

        # Notificar a todos que un nuevo usuario se ha unido
        await notificar_todos(f" {nombre} se ha unido al chat")

        async for mensaje in websocket:
            print(f" {nombre} dice: {mensaje}")
            await notificar_todos(mensaje)
    except websockets.exceptions.ConnectionClosed:
        nombre = clientes.get(websocket, "Usuario desconocido")
        print(f" {nombre} se ha desconectado inesperadamente")
    finally:
        # Notificar a todos que el usuario se ha desconectado
        nombre = clientes.pop(websocket, "Usuario desconocido")
        await notificar_todos(f" {nombre} se ha desconectado")

async def notificar_todos(mensaje):
    if clientes:
        await asyncio.gather(*(cliente.send(mensaje) for cliente in clientes))

async def iniciar_servidor():
    puerto = os.getenv('PORT', 5000)
    server = await websockets.serve(manejar_cliente, "0.0.0.0", int(puerto))
    print(f"🚀 Servidor WebSocket en ws://0.0.0.0:{puerto}")
    await server.wait_closed()

asyncio.run(iniciar_servidor())
