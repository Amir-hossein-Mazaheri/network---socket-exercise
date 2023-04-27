import logging
from socket import socket, AF_INET, SOCK_STREAM

from src.RequestHandler import RequestHandler
from src.Router import Router


class Node:
    __socket: socket
    __port: int
    __clients: list[RequestHandler] = []
    __route_handler: Router

    def __init__(self, route_handler: Router) -> None:
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__route_handler = route_handler

    def listen(self, port: int) -> None:
        self.__port = port

        # just makes sure app starts if the selected port was reserved before
        while True:
            try:
                self.__socket.bind(('127.0.0.1', self.__port))
                self.__socket.listen()

                break
            except OSError:
                self.__port += 1

    def start(self):
        logging.info(f"\n🚀 Node listening on port {self.__port}...\n")
        while True:
            try:
                (client_socket, _) = self.__socket.accept()
                self.__clients.append(RequestHandler(
                    client_socket, self.__route_handler))
            except KeyboardInterrupt:
                logging.info("You successfully stopped the node.")
                break
            except Exception as ex:
                logging.error(f"Something went wrong details:\n {ex}")
