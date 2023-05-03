import json
import logging
from urllib.parse import urlparse, parse_qs
from socket import socket
from threading import Thread


from src.HttpRequest import HttpRequest
from src.Router import Router


class RequestHandler:
    __thread: Thread
    __socket: socket
    __req: HttpRequest
    __route_handler: Router

    def __parser(self, data: bytes):
        (headers, body) = tuple(data.split(b"\r\n\r\n"))

        decoded_body = body.decode()

        splitted_headers = headers.split(b"\r\n")

        req_info = splitted_headers[0].decode().split(" ")

        method = req_info[0].upper()

        url = urlparse(req_info[1] or "")

        parsed_headers: dict[str, str] = {}

        for header in splitted_headers[1:]:
            splitted_header = header.decode().split(":")

            header_name = splitted_header[0].lower()

            parsed_headers[header_name] = ":".join(splitted_header[1:]).strip()

        content_type = parsed_headers.get('content-type')

        content_type_val = content_type.split(";")[0] if content_type else ""

        if content_type_val == 'application/json':
            decoded_body = json.loads(decoded_body)

        self.__req = HttpRequest(method, url.path, parse_qs(
            url.query), parsed_headers, decoded_body)

        return self.__req

    def __init__(self, socket: socket, route_handler: Router) -> None:
        self.__socket = socket
        self.__thread = Thread(target=self.handler, daemon=True)
        self.__route_handler = route_handler

        self.__thread.start()

    def handler(self):
        try:
            data = b''

            while req := self.__socket.recv(4096):
                data += req

                if len(req) < 4096:
                    break

            req = self.__parser(data)

            self.__route_handler.matcher(req, self.__socket)

        except Exception as ex:
            msg = f"Something went wrong while trying to handle http request:\n {ex}"

            logging.error(msg)

            socket = self.__socket

            socket.send(b"HTTP/1.1 500 Server Internal Error\r\n\r\n")
            socket.send(msg.encode())
            socket.close()
