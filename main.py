import os
import logging
from dotenv import load_dotenv

from src.PathScanner import PathScanner
from src.Node import Node
from src.Router import Router
from src.HttpRequest import HttpRequest
from src.utils import fill_nodes
from src.constants import MAX_PORT_NUMBER, MIN_PORT_NUMBER, NODES
from src.types import RouterContext

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
def index(req: HttpRequest, context: RouterContext):
    index_page_path = os.path.join(os.getcwd(), 'ui', 'dist', 'index.html')

    context["download"] = False

    with open(index_page_path, 'rb') as file:
        return file.read()


@router.get('/assets/:file')
def assets(req: HttpRequest, context: RouterContext):
    asset_path = os.path.join(
        os.getcwd(), 'ui', 'dist', 'assets', req.get_param('file'))

    context["download"] = False

    with open(asset_path, 'rb') as file:
        return file.read()


@router.get('/list')
def get_dir_list(req: HttpRequest, _):
    prefix = req.get_query_param('prefix')

    real_path = path

    if prefix:
        real_path = prefix[0]

    scanner = PathScanner(real_path)

    return scanner.scan()


@router.get('/path')
def get_path(req: HttpRequest, _):
    return {"path": path}


@router.get('/file')
def send_file(req: HttpRequest, context: RouterContext):
    path = req.get_query_param('path')

    if not path:
        return {"message": "should feed the url with path query param"}

    path = path[0]

    context["download"] = True

    with open(path, 'rb') as file:
        context["filename"] = file.name

        return file.read()


@router.get('/indicator')
def node_indicator(req: HttpRequest, _):
    return True


@router.get('/nodes')
def get_available_nodes(req: HttpRequest, _):
    if len(NODES) > 0:
        return NODES

    NODES.clear()

    fill_nodes(NODES)

    return NODES


@router.get('/refresh-nodes')
def refresh_nodes(req: HttpRequest, _):
    NODES.clear()

    fill_nodes(NODES)

    return NODES


node = Node(router)

node.listen(port)
node.start()
