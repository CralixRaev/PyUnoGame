import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.2.59", 5499))
data = {'type': 'register', 'username': 'user', 'password': 'test'}
s.send(pickle.dumps(data))
print(pickle.loads(s.recv(2048)))

