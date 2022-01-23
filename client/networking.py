import pickle
import socket

from classes.auth.exceptions import WrongCredentials
from classes.auth.user import User
from classes.cards.card import Card
from classes.decks.game_deck import GameDeck
from classes.game.game import Game


class Networking:
    """
    Networking-singleton для авторизации и обмена состояниями игры
    """

    def __init__(self, address: str = socket.gethostname(), port: int = 5499):
        self.current_game: Game = Game([], GameDeck())
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
        self.current_game = pickle.loads(self.sock.recv(4096))

    def throw_card(self, card: int | Card, ignore: bool = False) -> bool:
        data = {'type': 'throw', 'card': card, 'ignore': ignore}
        self.sock.sendall(pickle.dumps(data))
        return pickle.loads(self.sock.recv(2048))

    def get_card(self) -> bool:
        data = {'type': 'get_card'}
        self.sock.sendall(pickle.dumps(data))
        return pickle.loads(self.sock.recv(2048))

    def add_points(self, amount: int = 0) -> bool:
        data = {'type': 'add_points', 'amount': amount}
        self.sock.sendall(pickle.dumps(data))
        return pickle.loads(self.sock.recv(2048))

    def say_uno(self) -> bool:
        data = {'type': 'say_uno'}
        self.sock.sendall(pickle.dumps(data))
        return pickle.loads(self.sock.recv(2048))

    def get_user_from_game(self) -> User:
        return [user for user in self.current_game.users if user.id == self.authorized_user.id][0]

    def user_id(self, user) -> int:
        return self.current_game.users.index(user)


    @property
    def is_our_move(self) -> bool:
        return self.current_game.cur_user_index == self.user_id(self.get_user_from_game())

    def __del__(self):
        self.sock.close()
