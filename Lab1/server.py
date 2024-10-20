import socket
import threading


def handle_client(client_socket):
    while True:
        data = client_socket
        if not data:
            break
        data = data.decode('utf-8')
        if data.lower().strip() == 'quit':
            client_socket.send('closed'.encode('utf-8'))
            break
        print(f'Received: {data}')
        response = data[::-1].encode("utf-8q")
        client_socket.send(response)
        print(f"sent: {response}")
    client_socket.close()
    print("Connection to client closed")


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 49153)
    server.bind(server_address)
    server.listen(3)
    print(f'Server now listening on port: {server_address[1]}')
    while True:
        client_socket, client_address = server.accept()
        print(f'Accepted connection from {client_address[0]}:{client_address[1]}')
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


run_server()
