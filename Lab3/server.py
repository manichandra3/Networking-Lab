import socket
import threading


class Hub:
    def __init__(self):
        self.factory = []
        self.lock = threading.Lock()

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            data = data.decode('utf-8')
            ip = client_socket.getpeername()[0]
            port = client_socket.getpeername()[1]
            print(f'Received: {data} from IP: {ip} Port: {port}')
            response = data.encode("utf-8")
            with self.lock:
                for device in self.factory:
                    if device != client_socket:
                        device.send(response)
                        print(f"Sent: {response.decode('utf-8')} to address: {ip}:{port}")

        client_socket.close()
        with self.lock:
            self.factory.remove(client_socket)
        print("Connection to client closed")

    def run_server(self):
        hub_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', 49153)
        hub_server.bind(server_address)
        hub_server.listen(5)
        print(f'Server now listening on port: {server_address[1]}')

        while True:
            client_socket, client_address = hub_server.accept()
            print(f'Accepted connection from {client_address[0]}:{client_address[1]}')
            client_socket.sendall(str(client_address[1]).encode('utf-8'))
            with self.lock:
                self.factory.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()


server = Hub()
server.run_server()
