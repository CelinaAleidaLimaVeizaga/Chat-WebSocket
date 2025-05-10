# servidor.py
import asyncio
import websockets

clientes = {}  # websocket: nombre_usuario

async def manejar_cliente(websocket):
    try:
        nombre = await websocket.recv()  # Primer mensaje es el nombre de usuario
        clientes[websocket] = nombre
        mensaje_conexion = f"{nombre} se ha unido"
        print("🔔", mensaje_conexion)
        await notificar_a_todos(mensaje_conexion)

        async for mensaje in websocket:
            print(f"📩 Mensaje de {nombre}: {mensaje}")
            await notificar_a_todos(mensaje)

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if websocket in clientes:
            nombre = clientes[websocket]
            del clientes[websocket]
            mensaje_salida = f"{nombre} se ha desconectado"
            print("🔕", mensaje_salida)
            await notificar_a_todos(mensaje_salida)

async def notificar_a_todos(mensaje):
    if clientes:
        await asyncio.gather(*(ws.send(mensaje) for ws in clientes))

async def iniciar_servidor():
    server = await websockets.serve(manejar_cliente, "localhost", 6790)
    print("🚀 Servidor WebSocket en ws://localhost:6790")
    await server.wait_closed()

asyncio.run(iniciar_servidor())

