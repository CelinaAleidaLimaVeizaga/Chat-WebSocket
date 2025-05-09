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

import socket
import threading

def recibir_mensajes(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            print(mensaje)
        except:
            break

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55555))

nombre = input("Introduce tu nombre de usuario: ")
cliente.send(nombre.encode('utf-8'))

hilo_recibir = threading.Thread(target=recibir_mensajes, args=(cliente,))
hilo_recibir.start()

while True:
    try:
        mensaje = input()
        cliente.send(mensaje.encode('utf-8'))
    except:
        break
