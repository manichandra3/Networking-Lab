import socket
import threading
import time


def handle_client(client_socket):
    with open('data.txt', 'r') as file:
        sequence_number = 1

        for line in file:
            frame = f"{sequence_number}:{line}"
            if line[0] != '#':
                client_socket.send(frame.encode('utf-8'))
                wait_time = line[1]
            start = time.time()

            while True:
                try:
                    client_socket.settimeout(5)
                    ack = int(client_socket.recv(1024).decode('utf-8'))
                    if ack == sequence_number:
                        print(f"Received correct ACK: {ack}")
                        sequence_number = 1 - sequence_number
                        break
                    else:
                        print(f"Received incorrect ACK: {ack}, expected: {sequence_number}")
                        print(f"Dropped ack: {ack}")
                except socket.timeout:
                    print(f"ACK not received/Frame not sent, resending frame")
                    if line[0] != '#':
                        client_socket.send(frame.encode('utf-8'))
                        start = time.time()
                    else:
                        break

    client_socket.close()


class Server:
    def __init__(self, host='0.0.0.0', port=49513):
        self.host = host
        self.port = port

    def run_server(self):
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host, self.port)
        sender.bind(server_address)
        sender.listen(1)
        print(f'Server now listening on port: {server_address[1]}')
        while True:
            client_socket, client_address = sender.accept()
            print("-----------------------------------------------------------------")
            print(f'Accepted connection from {client_address[0]}:{client_address[1]}')
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()


if __name__ == "__main__":
    server = Server()
    server.run_server()
