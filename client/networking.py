import pickle
import socket

from classes.auth.exceptions import WrongCredentials
from classes.auth.user import User


# data = {'type': 'register', 'username': 'user', 'password': 'test'}
# data = {'type': 'login', 'username': 'user', 'password': 'test'}

class Networking:
    """
    Networking-singleton для авторизации и обмена состояниями игры
    """

    def __init__(self, address: str = socket.gethostname(), port: int = 5499):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.authorized_user = None
        self._connect(address, port)

    def _connect(self, address, port):
        self.sock.connect((address, port))

    def login(self, username, password) -> User:
        data = {'type': 'login', 'username': username, 'password': password}
        self.sock.sendall(pickle.dumps(data))
        answer = pickle.loads(self.sock.recv(2048))
        if type(answer) == dict:
            raise WrongCredentials(answer['message'])
        else:
            self.authorized_user = answer
            return answer

    def register(self, username, password) -> User:
        data = {'type': 'register', 'username': username, 'password': password}
        self.sock.sendall(pickle.dumps(data))
        answer = pickle.loads(self.sock.recv(2048))
        if type(answer) == dict:
            raise ValueError(answer['message'])
        else:
            self.authorized_user = answer
            return answer

    def __del__(self):
        self.sock.close()