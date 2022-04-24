import socket
import threading


host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print(f"El servidor esta corriendo en{host}:{port}")


clientes = []
nombres_usuarios = []


def broadcast(mensaje, _cliente):
    for cliente in clientes:
        if cliente != _cliente:
            cliente.send(mensaje)


def handle_messages(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            broadcast(mensaje,  cliente)
        except:
            indice = clientes.index(cliente)
            nombre = nombres_usuarios[indice]
            broadcast(f"Sistema: {nombre} se ha descoctado".encode(
                'utf-8'),  cliente)
            clientes.remove(cliente)
            nombres_usuarios.remove(nombre)
            cliente.close()
            break


def receive_connections():
    while True:
        cliente, direccion = server.accept()

        
        nombre = cliente.recv(1024).decode('utf-8')

        clientes.append(cliente)
        nombres_usuarios.append(nombre)

        print(f"{nombre} se ha conectado con {str(direccion)}")

        mensaje = f"Sistema: {nombre} se ha unido al chat".encode("utf-8")
        broadcast(mensaje,  cliente)
        cliente.send("Se ha conectado al servidor".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(cliente,))
        thread.start()


receive_connections()
