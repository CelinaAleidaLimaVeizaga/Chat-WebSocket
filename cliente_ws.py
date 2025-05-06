import asyncio
import websockets
import datetime

def formato_mensaje(remitente, mensaje):
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    return f"[{hora}] {remitente}: {mensaje}"

def color_mensaje(remitente, mensaje, es_cliente):
    color_usuario = "\033[94m" 
    color_otros = "\033[92m"  
    color_reset = "\033[0m"   
    
    if es_cliente:
        return f"{color_usuario}{formato_mensaje(remitente, mensaje)}{color_reset}"
    else:
        return f"{color_otros}{formato_mensaje(remitente, mensaje)}{color_reset}"

async def cliente():
    uri = "ws://localhost:6790"

    nombre = input("👉 Escribe tu nombre de usuario: ")
    if not nombre.strip():
        print("❌ Debes proporcionar un nombre de usuario para conectarte.")
        return  

    async with websockets.connect(uri) as websocket:
        print(f"✅ Conectado como {nombre}")

        async def recibir():
            try:
                async for mensaje in websocket:
                    if mensaje.startswith(f"{nombre}:"):
                        print(color_mensaje("Tú", mensaje, es_cliente=True))
                    else:
                        print(color_mensaje("Otro Usuario", mensaje, es_cliente=False))
            except websockets.exceptions.ConnectionClosed:
                print("❌ Conexión cerrada por el servidor")

        async def enviar():
            loop = asyncio.get_event_loop()
            while True:
                mensaje = await loop.run_in_executor(None, input, f"{nombre}: ")
                if mensaje.lower() == "salir":
                    print("🚪 Cerrando conexión...")
                    break
                mensaje_formateado = formato_mensaje("Tú", mensaje)
                print(f"{mensaje_formateado}") 
                await websocket.send(f"{nombre}: {mensaje}")  

        await asyncio.gather(recibir(), enviar())

asyncio.run(cliente())
