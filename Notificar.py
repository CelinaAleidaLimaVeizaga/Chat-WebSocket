import asyncio
import websockets

connected_users = set()

async def notify_users(message):
    if connected_users:  # Verifica que haya usuarios conectados
        await asyncio.wait([user.send(message) for user in connected_users])

async def handler(websocket, path):
    # Agrega el nuevo usuario a la lista de conectados
    connected_users.add(websocket)
    try:
        # Notifica a todos que un nuevo usuario se ha unido
        await notify_users("Un nuevo usuario se ha unido al chat.")
        async for message in websocket:
            # Aquí puedes manejar los mensajes entrantes de los usuarios
            pass
    finally:
        # El usuario se ha desconectado, remuévelo de la lista
        connected_users.remove(websocket)
        # Notifica a todos que un usuario se ha desconectado
        await notify_users("Un usuario se ha desconectado del chat.")

start_server = websockets.serve(handler, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

