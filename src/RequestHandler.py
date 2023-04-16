import json
import logging
from socket import socket
from threading import Thread
from time import sleep


from src.HttpRequest import HttpRequest


class RequestHandler:
    __thread: Thread
    __socket: socket
    __req: HttpRequest

    def __parser(self, data: bytes):
        (headers, body) = tuple(data.split(b"\r\n\r\n"))

        decoded_body = body.decode()

        splitted_headers = headers.split(b"\r\n")

        method = splitted_headers[0].decode().split(" ")[0].upper()

        parsed_headers: dict[str, str] = {}

        for header in splitted_headers[1:]:
            splitted_header = header.decode().split(":")

            header_name = splitted_header[0].lower()

            parsed_headers[header_name] = ":".join(splitted_header[1:]).strip()

        content_type = parsed_headers.get('content-type')

        content_type_val = content_type.split(";")[0] if content_type else ""

        if content_type_val == 'application/json':
            decoded_body = json.loads(decoded_body)

        self.__req = HttpRequest(method, parsed_headers, decoded_body)

        return self.__req

    def handler(self):
        try:
            data = b''

            while req := self.__socket.recv(4096):
                data += req

                sleep(0.001)

                if len(req) < 4096:
                    break

            parsed = self.__parser(data)

            print(parsed)

        except:
            logging.error(
                "Something went wrong while trying to handle http request")

    def __init__(self, socket: socket) -> None:
        self.__socket = socket
        self.__thread = Thread(target=self.handler)
        self.__thread.start()
