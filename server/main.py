import socket
import threading
import logging
from typing import Callable, NoReturn


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


class Server:
    """
    Сервер игры построенный с помощью Singleton паттерна
    """

    # Конечно, это ничего более чем просто демонстрация
    # учитывая, мою базу по сетям, я бы мог и написать эту историю поверх UDP,
    # сконструировать красивые пакетики, сделать сервер не блокирующим (т.е. асинхронным)
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
    def _client_thread(sock: socket.socket):
        print(sock.recv(2048).decode())
        sock.send("Hello-hello!".encode())

    def mainloop(self, client_thread: Callable = None) -> NoReturn:
        if not client_thread:
            client_thread = self._client_thread
        while True:
            client_socket, client_address = self.sock.accept()
            logging.info(f"New client {client_address}, starting client thread")
            thread = threading.Thread(target=client_thread, args=(client_socket,))
            thread.start()

    def __del__(self):
        self.sock.close()

if __name__ == '__main__':
    server = Server(address="192.168.2.59")
    server.mainloop()
