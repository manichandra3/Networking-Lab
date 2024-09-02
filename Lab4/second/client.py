import socket


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


c = socket.socket()
c.connect(('0.0.0.0', 49153))

while True:
    x = input("Enter the string: ")
    if not x:
        break
    stuffed_x = byte_stuff(x.encode('utf-8'))
    c.send(stuffed_x)
    response = c.recv(1024).decode('utf-8')
    print("Stuffed data from server:", response)

c.close()
