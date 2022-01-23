import logging
import pickle
import socket
import sqlite3
import threading
from typing import Callable, NoReturn

from auth import Authorization, WrongCredentials
from classes.auth.user import User
from classes.decks.game_deck import GameDeck
from classes.game.game import Game

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


class Server:
    """
    Сервер игры построенный с помощью Singleton паттерна
    """

    # Конечно, это ничего более чем просто демонстрация
    # учитывая, мою базу по сетям, я бы мог и написать эту историю поверх UDP,
    # сконструировать красивый протокол, сделать сервер не блокирующим (т.е. асинхронным)
    # но времени мало + мне лень, а также в лицее нам про асинхронность почему-то не рассказывают)
    def __init__(self, address: str = socket.gethostname(), port: int = 5499):
        self.current_game = Game([], GameDeck())
        self.current_game.deck.init_random()
        self.threads = []
        # порт в моём случае выбран абсолютно случайно
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._bind(address, port)
        self._listen()

    def _bind(self, address: str, port: int):
        self.sock.bind((address, port))

    def _listen(self, max_clients: int = 3):
        self.sock.listen(max_clients)

    def __register(self, authorization, username: str, password: str, address: tuple[str, int]) -> \
            tuple[User, Game] | dict:
        try:
            user = authorization.register(username, password)
            user.deck.init_random()
            user.address = address
            self.current_game.append_user(user)
            logging.debug(f"Successfully registered user {username}")
            return user, self.current_game
        except sqlite3.IntegrityError:
            return {'type': 'error',
                    'message': "Такой пользователь уже существует"}
        except ValueError as e:
            return {'type': 'error',
                    'message': e}
        except Exception as e:
            logging.exception("Exception while trying to register", exc_info=e)
            return {'type': 'error',
                    'message': "Техническая ошибка, проверьте логи сервера"}

    def __login(self, authorization, username: str, password: str, address: tuple[str, int]) -> \
            tuple[User, Game] | dict:
        try:
            user = authorization.login(username, password)
            user.deck.init_random()
            user.address = address
            self.current_game.append_user(user)
            logging.debug(f"Successfully authorized user {username}")
            return user, self.current_game
        except WrongCredentials:
            return {'type': 'error',
                    'message': "Пользователя с таким логином/паролем не существует"}
        except ValueError as e:
            return {'type': 'error',
                    'message': e}
        except Exception as e:
            logging.exception("Exception while trying to login", exc_info=e)
            return {'type': 'error',
                    'message': "Техническая ошибка, проверьте логи сервера"}

    def __fetch(self):
        return self.current_game

    def __update(self, data: dict):
        pass
        # match data["update_type"]:

    def __throw(self, user, card: int) -> bool:
        card_object = user.deck.cards[card]
        result = self.current_game.deck.append_card(user.deck.cards[card])
        if result:
            card_object.move(self.current_game)
            user.deck.cards.pop(card)
            print(self.current_game.cur_user_index)
            self.current_game.next_player()
        return result

    @staticmethod
    def __get_card(self, user) -> bool:
        user.deck.random_cards()
        return True

    def _client_thread(self, sock: socket.socket, address: tuple[str, int]):
        authorization = Authorization('../database.db')
        while True:
            data = sock.recv(2048)
            if not data:
                logging.info(f"Client {address} closed connection, so we are closing it too")
                try:
                    self.current_game.users.remove(
                        [user for user in self.current_game.users if user.address == address][0])
                except IndexError:
                    logging.warning(f"User with address {address} didnt logon, so we cant remove it")
                sock.close()
                break
            loaded_data: dict = pickle.loads(data)

            answer = None
            # python 3.10 goes brrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
            match loaded_data['type']:
                case "register":
                    answer = username, password = loaded_data['username'], loaded_data['password']
                    self.__register(authorization, username, password, address)
                case "login":
                    username, password = loaded_data['username'], loaded_data['password']
                    answer = self.__login(authorization, username, password, address)
                case "fetch":
                    answer = self.__fetch()
                case "update":
                    self.__update(loaded_data)
                    answer = self.__fetch()
                case "throw":
                    answer = self.__throw(self._user_by_address(address), loaded_data['card'])
                case "get_card":
                    answer = self.__get_card(self._user_by_address(address))
            sock.sendall(pickle.dumps(answer))

    def _user_by_address(self, address: tuple[str, int]):
        return [user for user in self.current_game.users if user.address == address][0]

    def mainloop(self, client_thread: Callable = None) -> NoReturn:
        if not client_thread:
            client_thread = self._client_thread
        while True:
            client_socket, client_address = self.sock.accept()
            logging.info(f"New client {client_address}, starting client thread")
            thread = threading.Thread(target=client_thread, args=(client_socket, client_address))
            self.threads.append(thread)
            thread.start()

    def __del__(self):
        self.sock.close()


if __name__ == '__main__':
    server = Server(address='127.0.0.1')
    server.mainloop()
