import socket
import sys


def custom_decode(data: str) -> list[str]:
    res = []
    i = 0
    while i < len(data):
        j = i
        while data[j] != '#':
            j += 1
        length = int(data[i:j])
        i = j + 1
        res.append(data[i:i + length])
        i += length
    return res


def custom_encode(strs: list[str]) -> str:
    res = ""
    for s in strs:
        res += str(len(s)) + "#" + s
    return res


class Client:
    MAXLINE = 200

    def __init__(self, ip, port):
        self.server_address = (ip, port)
        self.sock = None

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(self.server_address)
            print("Connection successful")
        except socket.error as e:
            print(f"Connection error: {e}", file=sys.stderr)
            sys.exit(1)

    def run(self):
        try:
            while True:
                send_line = input("Enter the message to send: ")
                send_list = ["client_id", send_line]
                encoded_send_line = custom_encode(send_list)

                if not self.sock:
                    print("Connection with the server failed!")
                    break

                self.sock.sendall(encoded_send_line.encode())

                recv_line = self.sock.recv(1024).decode()
                recv_list = custom_decode(recv_line)

                if recv_list:
                    recv_addr = recv_list[0]
                    recv_message = recv_list[1]
                    print(f"Message received from {recv_addr}: {recv_message}")
                else:
                    print("Server closed connection", file=sys.stderr)
                    break
        except socket.error as e:
            print(f"Socket error: {e}", file=sys.stderr)
        finally:
            if self.sock:
                self.sock.close()


client = Client('0.0.0.0', 49153)
client.connect()
client.run()
