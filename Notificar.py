import socket
import threading

# Lista para almacenar conexiones activas
clientes = []
nombres = []

def notificar_a_todos(mensaje):
    for cliente in clientes:
        cliente.send(mensaje.encode('utf-8'))

def manejar_cliente(cliente):
    nombre = cliente.recv(1024).decode('utf-8')
    nombres.append(nombre)
    clientes.append(cliente)

    notificar_a_todos(f"{nombre} se ha unido")

    while True:
        try:
            mensaje = cliente.recv(1024)
            if not mensaje:
                break
        except:
            break

    clientes.remove(cliente)
    nombres.remove(nombre)
    cliente.close()
    notificar_a_todos(f"{nombre} se ha desconectado")

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('127.0.0.1', 55555))
    servidor.listen()

    print("Servidor corriendo en 127.0.0.1:55555...")

    while True:
        cliente, direccion = servidor.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(cliente,))
        hilo.start()

iniciar_servidor()


asyncio.run(iniciar_servidor())

