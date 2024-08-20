import socket
import sys
import threading


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
        self.unique_id = None

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(self.server_address)
            print("Connection successful")

            self.unique_id = self.sock.recv(1024).decode("utf-8")
            if self.unique_id:
                print(f"Unique ID: {self.unique_id}")
        except socket.error as e:
            print(f"Connection error: {e}", file=sys.stderr)
            sys.exit(1)

    def listen_for_messages(self):
        try:
            while True:
                recv_line = self.sock.recv(1024).decode()
                if not recv_line:
                    print("Connection closed by the server")
                    break

                recv_list = custom_decode(recv_line)
                if recv_list:
                    src_addr = recv_list[0]
                    dst_addr = recv_list[1]
                    recv_message = recv_list[2]
                    if self.unique_id == dst_addr:
                        print(f"\nMessage received from {src_addr}: {recv_message}")
                    else:
                        print(f"\nMessage dropped! {src_addr} does not match "
                              f"{dst_addr}")
        except socket.error as e:
            print(f"Socket error while receiving: {e}", file=sys.stderr)
        finally:
            if self.sock:
                self.sock.close()

    def send_messages(self):
        try:
            while True:
                send_line = input("Enter the message to send (or 'exit' to quit): ")
                if send_line.lower() == 'exit':
                    print("Exiting...")
                    break

                dst_addr = input("Enter the port to send: ")
                send_list = [str(self.unique_id), dst_addr, send_line]
                encoded_send_line = custom_encode(send_list)

                if not self.sock:
                    print("Connection with the server failed!")
                    break

                self.sock.sendall(encoded_send_line.encode())
        except socket.error as e:
            print(f"Socket error while sending: {e}", file=sys.stderr)
        finally:
            if self.sock:
                self.sock.close()

    def run(self):
        listener_thread = threading.Thread(target=self.listen_for_messages)
        listener_thread.daemon = True
        listener_thread.start()

        self.send_messages()
        listener_thread.join()


client = Client('127.0.0.1', 49153)
client.connect()
client.run()
