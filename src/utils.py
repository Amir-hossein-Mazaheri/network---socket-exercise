import json
from socket import socket

from src.constants import MIN_PORT_NUMBER, MAX_PORT_NUMBER, HOST


def fill_nodes(nodes: list):
    for port in range(MIN_PORT_NUMBER, MAX_PORT_NUMBER + 1):
        client_socket = socket()

        try:
            client_socket.settimeout(0.1)
            client_socket.connect((HOST, port))

            client_socket.send(b"GET /indicator HTTP/1.1\r\n\r\n")

            data = b""

            while True:
                d = client_socket.recv(4096)
                data += d

                if not d:
                    break

            if json.loads(data.decode().split("\r\n\r\n")[1]):
                nodes.append(f"{HOST}:{port}")
        except Exception as ex:
            continue
        finally:
            client_socket.close()
