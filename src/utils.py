import json
import mimetypes
from socket import socket

from src.constants import MIN_PORT_NUMBER, MAX_PORT_NUMBER, HOST


mimetypes.init()


def fill_nodes(nodes: list):
    for port in range(MIN_PORT_NUMBER, MAX_PORT_NUMBER + 1):
        client_socket = socket()

        try:
            client_socket.settimeout(0.01)
            client_socket.connect((HOST, port))

            client_socket.send(b"GET /indicator HTTP/1.1\r\n\r\n")

            data = b""

            while True:
                d = client_socket.recv(4096)
                data += d

                if not d:
                    break

            if json.loads(data.decode().split("\r\n\r\n")[1]):
                nodes.append(f"http://localhost:{port}")
        except Exception as ex:
            continue
        finally:
            client_socket.close()


ext_to_mime = {
    "text/x-script.python": ["py"],
    "text/html": ["html", "htm"],
    "text/css": ["css"],
    "application/js": ["js"],
    "image/jpeg": ["jpeg", "jpg"],
    "image/gif": ["gif"],
    "image/png": ["png"],
    "image/x-icon": ["ico"],
    "application/json": ["json"],
    "application/pdf": ["pdf"],
    "application/msword": ["doc"],
    "application/x-rar-compressed": ["rar"],
    "audio/mpeg": ["mp3"],
    "video/mp4": ["mp4"],
}


def mime_detector(filename: str):
    file_ext = filename.split("\\")[-1].split(".")[-1]

    mime_type = mimetypes.types_map.get(f".{file_ext}") or 'text/plain'

    if mime_type == 'text/plain':
        for key, val in ext_to_mime.items():
            if file_ext in val:
                mime_type = key
                break

    return mime_type
