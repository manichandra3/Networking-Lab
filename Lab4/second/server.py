import socket
import threading


def byte_stuff(data):
    ESC = b'1101'
    FLAG = b'01111110'
    ans = b""
    i = 0
    while i < len(data):
        if data[i:i + len(FLAG)] == FLAG:
            ans += ESC + FLAG
            i += len(FLAG)
        elif data[i:i + len(ESC)] == ESC:
            ans += ESC + ESC
            i += len(ESC)
        else:
            ans += bytes([data[i]])
            i += 1
    return FLAG + ans + FLAG


def byte_unstuff(stuffed_data):
    ESC = b'1101'
    FLAG = b'11011110'
    ans = b''
    data = stuffed_data[len(FLAG):-len(FLAG)]

    i = 0
    while i < len(data):
        if data[i:i + len(ESC)] == ESC:
            i += len(ESC)
            if data[i:i + len(FLAG)] == FLAG:
                ans += FLAG
                i += len(FLAG)
            elif data[i:i + len(ESC)] == ESC:
                ans += ESC
                i += len(ESC)
            else:
                raise ValueError("Invalid stuffing sequence")
        else:
            ans += bytes([data[i]])
            i += 1

    return ans


def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        unstuffed_data = byte_unstuff(data).decode('utf-8')
        if unstuffed_data.lower().strip() == 'quit':
            client_socket.send(byte_stuff(b'closed'))
            break
        print(f'Received: {unstuffed_data}')
        response = byte_stuff(unstuffed_data.encode("utf-8"))
        client_socket.send(response)
        print(f"Sent: {response.decode('utf-8')}")
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
