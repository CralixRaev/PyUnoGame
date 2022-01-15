import pickle
import socket
import sqlite3
import threading
import logging
from typing import Callable, NoReturn
from auth import Authorization, WrongCredentials

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
        # порт в моём случае выбран абсолютно случайно
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._bind(address, port)
        self._listen()

    def _bind(self, address: str, port: int):
        self.sock.bind((address, port))

    def _listen(self, max_clients: int = 4):
        self.sock.listen(max_clients)

    @staticmethod
    def _client_thread(sock: socket.socket, address: tuple[str, int]):
        authorization = Authorization('../database.db')
        while True:
            data = sock.recv(2048)
            if not data:
                logging.info(f"Client {address} closed connection, so we are closing it too")
                sock.close()
                break
            loaded_data: dict = pickle.loads(data)

            answer = None
            # python 3.10 goes brrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
            match loaded_data['type']:
                case "register":
                    username, password = loaded_data['username'], loaded_data['password']
                    try:
                        authorization.register(username, password)
                        answer = {'type': 'register',
                                  'message': 'Пользователь успешно зарегистрирован'}
                    except sqlite3.IntegrityError:
                        answer = {'type': 'error',
                                  'message': "Такой пользователь уже существует"}
                    except Exception as e:
                        logging.exception("Exception while trying to register", exc_info=e)
                        answer = {'type': 'error',
                                  'message': "Техническая ошибка, проверьте логи сервера"}
                case "login":
                    username, password = loaded_data['username'], loaded_data['password']
                    try:
                        user = authorization.login(username, password)
                        answer = user
                    except WrongCredentials:
                        answer = {'type': 'error',
                                  'message': "Пользователя с таким логином/паролем не существует"}
                    except Exception as e:
                        logging.exception("Exception while trying to login", exc_info=e)
                        answer = {'type': 'error',
                                  'message': "Техническая ошибка, проверьте логи сервера"}
            sock.sendall(pickle.dumps(answer))

    def mainloop(self, client_thread: Callable = None) -> NoReturn:
        if not client_thread:
            client_thread = self._client_thread
        while True:
            client_socket, client_address = self.sock.accept()
            logging.info(f"New client {client_address}, starting client thread")
            thread = threading.Thread(target=client_thread, args=(client_socket, client_address))
            thread.start()

    def __del__(self):
        self.sock.close()


if __name__ == '__main__':
    server = Server(address="192.168.2.59")
    server.mainloop()
