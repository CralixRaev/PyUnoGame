import pickle
import socket

from classes.auth.exceptions import WrongCredentials
from classes.auth.user import User


# data = {'type': 'register', 'username': 'user', 'password': 'test'}
# data = {'type': 'login', 'username': 'user', 'password': 'test'}
from classes.decks.game_deck import GameDeck
from classes.game.game import Game


class Networking:
    """
    Networking-singleton для авторизации и обмена состояниями игры
    """

    def __init__(self, address: str = socket.gethostname(), port: int = 5499):
        self.current_game: Game = Game([], GameDeck())
        self.current_game.deck.init_random()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.authorized_user = None
        self._connect(address, port)

    def _connect(self, address, port):
        self.sock.connect((address, port))

    def login(self, username, password) -> User:
        data = {'type': 'login', 'username': username, 'password': password}
        self.sock.sendall(pickle.dumps(data))
        answer = user, game = pickle.loads(self.sock.recv(2048))
        if type(answer) == dict:
            raise WrongCredentials(answer['message'])
        else:
            self.authorized_user = user
            self.current_game = game
            return answer

    def register(self, username, password) -> User:
        data = {'type': 'register', 'username': username, 'password': password}
        self.sock.sendall(pickle.dumps(data))
        answer = user, game = pickle.loads(self.sock.recv(2048))
        if type(answer) == dict:
            raise ValueError(answer['message'])
        else:
            self.authorized_user = user
            self.current_game = game
            return answer

    def fetch(self):
        data = {'type': 'fetch'}
        self.sock.sendall(pickle.dumps(data))
        self.current_game = pickle.loads(self.sock.recv(2048))

    def get_user_from_game(self) -> User:
        return [user for user in self.current_game.users if user.id == self.authorized_user.id][0]

    def __del__(self):
        self.sock.close()