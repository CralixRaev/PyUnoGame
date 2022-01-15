import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.2.59", 5499))
s.send("Hello!".encode())
print(s.recv(2048).decode())
