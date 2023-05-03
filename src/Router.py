import json
from typing import TypeAlias, Callable
from socket import socket

from src.HttpRequest import HttpRequest
from src.HttpResponse import HttpResponse
from src.HttpError import HttpError

Route: TypeAlias = tuple[str, str, Callable]


class Router:
    __routes: list[Route] = []
    __not_found = None
    __cors: bool

    def __init__(self, cors) -> None:
        self.__not_found = lambda req: {"message": "invalid request"}
        self.__cors = cors

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

    def not_found(self, func):
        self.__not_found = func

    def matcher(self, req: HttpRequest, socket: socket):
        try:
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
                        req.append_params(
                            dynamic_route, splitted_req_route[-1])

                    res = HttpResponse()
                    body = callback(req, res)

                    try:
                        body = json.dumps(body).encode()
                    except (TypeError, OverflowError):
                        pass

                    socket.send(f"HTTP/1.1 {res.get_status()} OK\r\n".encode())

                    for key, value in res.get_headers().items():
                        socket.send(f"{key}: {value}\r\n".encode())

                    if self.__cors:
                        socket.send(b"Access-Control-Allow-Origin: *\r\n")

                    socket.send(b"\r\n\r\n")
                    socket.send(body)

                    socket.close()

                    return

            res = HttpResponse()
            value = self.__not_found(req, res)

            body = json.dumps(value).encode()

            socket.send(b"HTTP/1.1 404 Not Found\n\n")
            socket.send(body)

            socket.close()

        except HttpError as e:
            socket.send(f"HTTP/1.1 {e.status} {e.msg}\r\n\r\n".encode())

            body = {
                "status": e.status,
                "message": e.msg,
                "detail": e.detail
            }

            socket.send(json.dumps(body).encode())

            socket.close()
