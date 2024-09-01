import socket
import threading
import time
# RFC-3396: 1.4.1:
#    A sender using stop-and-wait ARQ (sometimes known as 'Idle ARQ'
#    [LIN93]) transmits a single frame and then waits for an
#    acknowledgement from the receiver for that frame.
#    The sender then either continues transmission with the next frame,
#    or repeats transmission of the same frame if the acknowledgement
#    indicates that the original frame was lost or corrupted.
#    Stop and Wait ARQ is generally good for networks with low bandwidth-delay product(volume).


def handle_client(client_socket):
    sequence_number = 1

    with open('data.txt', 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue

            frame = f"{sequence_number}:{line.strip()}"
            client_socket.send(frame.encode('utf-8'))
            print(f"Sent frame: {frame}")

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
                except socket.timeout:
                    print(f"ACK not received. Resending frame: {frame}")
                    client_socket.send(frame.encode('utf-8'))

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
