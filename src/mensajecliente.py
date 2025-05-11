# mensaje_cliente.py
import asyncio
import websockets
import datetime

historial = []

def formato_mensaje(mensaje):
    hora = datetime.datetime.now().strftime("%H:%M:%S")
    return f"[{hora}] {mensaje}"

def mostrar_historial():
    print("\n=== Historial de Mensajes ===")
    for entrada in historial:
        print(entrada)
    print("=============================\n")

async def cliente_historial():
    #uri = "ws://localhost:6790"
    uri = "wss://chat-websocket-sis-colab.onrender.com"

    print("🟢 Cliente visualizador conectado al historial")
    async with websockets.connect(uri) as websocket:
        try:
            async for mensaje in websocket:
                entrada = formato_mensaje(mensaje)
                historial.append(entrada)
                mostrar_historial()
        except websockets.exceptions.ConnectionClosed:
            print("❌ Conexión cerrada por el servidor")

asyncio.run(cliente_historial())