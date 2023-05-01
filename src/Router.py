import json
from typing import TypeAlias, Callable
from socket import socket

from src.HttpRequest import HttpRequest
from src.types import RouterContext

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
        # it is just a context for passing additional info to the mather
        # route function return value could be transformed into something that
        # we can delete the context but this way is cleaner
        context: RouterContext = {}

        for route, method, callback in self.__routes:
            real_req_route = ""
            dynamic_route = None
            splitted_route = route.split(":")
            splitted_req_route = req.get_route().split("/")

            try:
                dynamic_route = splitted_route[1]

                real_req_route = "/".join(splitted_req_route[:-1])
            except IndexError:
                real_req_route = "/".join(splitted_req_route)

            if splitted_route[0].rstrip("/") == real_req_route.rstrip("/") and method == req.get_method():
                if dynamic_route:
                    req.add_to_params(
                        dynamic_route, splitted_req_route[-1])

                value = callback(req, context)

                body = value

                if type(value) != bytes:
                    body = json.dumps(value).encode()

                socket.send(b"HTTP/1.1 200 OK\r\n")

                if type(value) == bytes:
                    socket.send(
                        ("Content-Type:" + context["mime"] + "\r\n").encode())

                    if context.get("download"):
                        socket.send(
                            f"content-disposition: attachment; filename={context.get('filename')}\r\n".encode())
                else:
                    socket.send(b"Content-Type:application/json\r\n")

                socket.send(b"Access-Control-Allow-Origin: *\r\n\r\n")
                socket.send(body)

                socket.close()

                return

        value = self.__not_found(req)

        body = json.dumps(value).encode()

        socket.send(b"HTTP/1.1 200 OK\n\n")
        socket.send(body)

        socket.close()
