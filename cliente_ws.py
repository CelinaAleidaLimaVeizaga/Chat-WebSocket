import asyncio
import websockets

async def cliente():
    uri = "ws://localhost:6790"  # <-- Asegurate que el puerto coincida con el del servidor
    nombre = input("👉 Escribe tu nombre de usuario: ")

    async with websockets.connect(uri) as websocket:
        print(f"✅ Conectado como {nombre}")

        async def recibir():
            try:
                async for mensaje in websocket:
                    print(f"\n💬 {mensaje}")
            except websockets.exceptions.ConnectionClosed:
                print("❌ Conexión cerrada por el servidor")

        async def enviar():
            loop = asyncio.get_event_loop()
            while True:
                mensaje = await loop.run_in_executor(None, input, f"{nombre}: ")
                if mensaje.lower() == "salir":
                    print("🚪 Cerrando conexión...")
                    break
                await websocket.send(f"{nombre}: {mensaje}")

        await asyncio.gather(recibir(), enviar())

asyncio.run(cliente())
 