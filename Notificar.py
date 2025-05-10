import asyncio
import websockets

clientes = set()
nombres = {}  # Asocia cada websocket a su nombre

async def manejar_cliente(websocket):
    print("🔌 Cliente conectado")
    clientes.add(websocket)

    try:
        # Espera el primer mensaje como nombre de usuario
        nombre = await websocket.recv()
        nombres[websocket] = nombre

        # Notifica a todos que el usuario se ha unido
        mensaje_union = f"🔔 {nombre} se ha unido al chat"
        await notificar_a_todos(mensaje_union)

        # Escucha los mensajes normalmente
        async for mensaje in websocket:
            print("📩 Mensaje recibido:", mensaje)
            for cliente in clientes:
                await cliente.send(mensaje)

    except websockets.exceptions.ConnectionClosed:
        print("⚠️ Cliente desconectado inesperadamente")

    finally:
        clientes.remove(websocket)
        nombre = nombres.get(websocket, "Usuario desconocido")
        nombres.pop(websocket, None)

        # Notifica a todos que el usuario se fue
        mensaje_salida = f"👋 {nombre} se ha desconectado"
        await notificar_a_todos(mensaje_salida)

        print(f"👋 Cliente '{nombre}' desconectado")

async def notificar_a_todos(mensaje):
    if clientes:
        await asyncio.gather(*(cliente.send(mensaje) for cliente in clientes))

async def iniciar_servidor():
    server = await websockets.serve(manejar_cliente, "localhost", 6790)
    print("🚀 Servidor WebSocket en ws://localhost:6790")
    await server.wait_closed()

asyncio.run(iniciar_servidor())
