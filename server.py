import socket
import threading

HOST = '192.168.1.124'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()
clients = []
names = []


def broadcast(messages):
    for client in clients:
        client.send(messages)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{names[clients.index(client)]}: {message}")

            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            names.remove(name)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}!')

        client.send("NAME".encode('utf-8'))
        name = client.recv(1024)

        names.append(name)
        clients.append(client)

        print(f"new connection: {name} joined")
        broadcast(f"new connection: {name} joined!\n".encode('utf-8'))
        client.send("connected to server".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('server is running...')
receive()
