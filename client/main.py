import socket
import pickle

from classes.auth.user import User


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.2.59", 5499))
# data = {'type': 'register', 'username': 'user', 'password': 'test'}
data = {'type': 'login', 'username': 'user', 'password': 'tesst'}
s.send(pickle.dumps(data))
print(pickle.loads(s.recv(2048)))

