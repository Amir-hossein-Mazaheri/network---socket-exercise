import json
from typing import TypeAlias, Callable
from socket import socket

from src.HttpRequest import HttpRequest

Route: TypeAlias = tuple[str, str, Callable]


class Router:
    __routes: list[Route] = []
    __not_found = None

    def __init__(self) -> None:
        self.__not_found = lambda req: {"message": "invalid request"}

    def get(self, route: str):
        def wrapper(func):
            self.__routes.append((route, "GET", func))

        return wrapper

    def post(self, route: str):
        def wrapper(func):
            self.__routes.append((route, "POST", func))

        return wrapper

    def put(self, route: str):
        def wrapper(func):
            self.__routes.append((route, "PUT", func))

        return wrapper

    def patch(self, route: str):
        def wrapper(func):
            self.__routes.append((route, "PATCH", func))

        return wrapper

    def not_found(self):
        def wrapper(func):
            self.__not_found = func

        return wrapper

    def matcher(self, req: HttpRequest, socket: socket):
        for route, method, callback in self.__routes:
            if route == req.get_route() and method == req.get_method():
                value = callback(req)

                body = value

                if type(value) != bytes:
                    body = json.dumps(value).encode()

                socket.send(b"HTTP/1.1 200 OK\n\n")
                socket.send(body)

                socket.close()

                return

        value = self.__not_found(req)

        body = json.dumps(value).encode()

        socket.send(b"HTTP/1.1 200 OK\n\n")
        socket.send(body)

        socket.close()
