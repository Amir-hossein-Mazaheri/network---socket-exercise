import os
import logging
import json
from dotenv import load_dotenv
from socket import socket

from src.PathScanner import PathScanner
from src.Server import Server
from src.Router import Router
from src.HttpRequest import HttpRequest
from src.utils import fill_nodes
from src.constants import MAX_PORT_NUMBER, MIN_PORT_NUMBER, NODES

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


load_dotenv()


port = None

while True:
    port = int(
        input("Which port do you want to use should be between 5500 and 5600: "))

    if MIN_PORT_NUMBER <= port <= MAX_PORT_NUMBER:
        break

router = Router()

path = fr"{input('Which path of your computer do you want to share (path should be absolute): ')}"


@router.get('/')
def index(req: HttpRequest):
    index_page_path = os.path.join(os.getcwd(), 'ui', 'dist', 'index.html')

    with open(index_page_path, 'rb') as file:
        return file.read()


@router.get('/assets/:file')
def assets(req: HttpRequest):
    asset_path = os.path.join(
        os.getcwd(), 'ui', 'dist', 'assets', req.get_param('file'))

    with open(asset_path, 'rb') as file:
        return file.read()


@router.get('/list')
def get_dir_list(req: HttpRequest):
    prefix = req.get_query_param('prefix')

    real_path = path

    if prefix:
        real_path = prefix[0]

    scanner = PathScanner(real_path)

    return scanner.scan()


@router.get('/path')
def get_path(req: HttpRequest):
    return {"path": path}


@router.get('/file')
def send_file(req: HttpRequest):
    path = req.get_query_param('path')

    if not path:
        return {"message": "should feed the url with path query param"}

    path = path[0]

    with open(path, 'rb') as file:
        return file.read()


@router.get('/indicator')
def node_indicator(req: HttpRequest):
    return True


@router.get('/nodes')
def get_available_nodes(req: HttpRequest):
    if len(NODES) > 0:
        return NODES

    NODES.clear()

    fill_nodes(NODES)

    return NODES


@router.get('/refresh-nodes')
def refresh_nodes(req: HttpRequest):
    NODES.clear()

    fill_nodes(NODES)

    return NODES


server = Server(router)

server.listen(port)
server.start()
