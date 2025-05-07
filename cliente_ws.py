import asyncio 
import websockets
import datetime
import random

# Función para estblecer el formato del mensaje con la hora y el remitente
def formato_mensaje(remitente, mensaje):
    hora = datetime.datetime.now().strftime("%H:%M:%S") 
    return f"[{hora}] {remitente}: {mensaje}"

# Función para agregar color al mensaje según si es del cliente o de otro usuario
def color_mensaje(remitente, mensaje, es_cliente):
    color_usuario = "\033[94m"
    color_otros = "\033[92m" 
    color_reset = "\033[0m"

    # Devuelve el mensaje con el color adecuado según el remitente
    if es_cliente:
        return f"{color_usuario}{formato_mensaje(remitente, mensaje)}{color_reset}"
    else:
        return f"{color_otros}{formato_mensaje(remitente, mensaje)}{color_reset}"

# Función principal que gestiona la conexión WebSocket y el chat
async def cliente():
    uri = "ws://localhost:6790" 

    nombre = input("👉 Escribe tu nombre de usuario: ") 
    if not nombre.strip():

        #Si no escribe ningun nombre de usuario, se asigna uno aleatorio : "Usuario" + "numero random"
        numRandom= random.randint(100, 999)
        nombre = f"Usuario_{numRandom}"
        print(f"Se te asigno automaticamente el nombre de : {nombre}")

        #print("❌ Debes proporcionar un nombre de usuario para conectarte.")
        #return  

    # Establece la conexión WebSocket con el servidor
    async with websockets.connect(uri) as websocket:
        print(f"✅ Conectado como {nombre}") 

        # Función para recibir mensajes de otros usuarios
        async def recibir():
            try:
                async for mensaje in websocket:  # Escucha los mensajes del servidor
                    if mensaje.startswith(f"{nombre}:"):  # Si el mensaje es del cliente, se destaca
                        print(color_mensaje("Tú", mensaje, es_cliente=True))
                    else:  # Los mensajes de otros usuarios se muestran de forma diferente
                        print(color_mensaje("Otro Usuario", mensaje, es_cliente=False))
            except websockets.exceptions.ConnectionClosed:  # Si la conexión se cierra, muestra un error
                print("❌ Conexión cerrada por el servidor")

        # Función para enviar mensajes al servidor
        async def enviar():
            loop = asyncio.get_event_loop()  # Obtiene el loop de eventos de asyncio
            while True:
                mensaje = await loop.run_in_executor(None, input, f"{nombre}: ")  # Solicita un mensaje al usuario
                if mensaje.lower() == "salir":  # Si el usuario escribe "salir", termina la conexión
                    print("🚪 Cerrando conexión...")
                    break
                mensaje_formateado = formato_mensaje("Tú", mensaje)  # Formatea el mensaje con la hora
                print(f"{mensaje_formateado}")  # Muestra el mensaje antes de enviarlo
                await websocket.send(f"{nombre}: {mensaje}")  # Envía el mensaje al servidor WebSocket

        # Ejecuta las funciones de recibir y enviar mensajes simultáneamente
        await asyncio.gather(recibir(), enviar())

# Ejecuta la función principal para iniciar el cliente
asyncio.run(cliente())