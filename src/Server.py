import logging
from socket import socket, AF_INET, SOCK_STREAM

from src.RequestHandler import RequestHandler


class Server:
    __socket: socket
    __port: int
    __clients: list[RequestHandler] = []

    def __init__(self) -> None:
        self.__socket = socket(AF_INET, SOCK_STREAM)

    def listen(self, port: int) -> None:
        self.__port = port

        while True:
            try:
                self.__socket.bind(('127.0.0.1', self.__port))
                self.__socket.listen()

                break
            except OSError:
                self.__port += 1

    def start(self):
        logging.info(f"\n🚀 Server listening on port {self.__port}...\n")
        try:
            while True:
                (client_socket, _) = self.__socket.accept()
                self.__clients.append(RequestHandler(client_socket))
        except KeyboardInterrupt:
            logging.info("You successfully stopped the server.")
            raise
        except Exception as ex:
            logging.error(f"Something went wrong details:\n {ex}")
