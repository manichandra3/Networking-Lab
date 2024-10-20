import socket

c = socket.socket()
c.connect(('192.168.42.16', 5555))

name = input("Enter your name: ")
c.send(bytes(name, 'utf-8'))

while True:
    x = input("Enter the string: ")
    if not x:
        break
    c.send(bytes(x, 'utf-8'))
    print("Reversed string from server:", c.recv(1024).decode())

c.close()
