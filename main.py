import os
import logging

from src.PathScanner import PathScanner
from src.Server import Server
from src.HttpRequest import HttpRequest
from src.HttpResponse import HttpResponse
from src.HttpError import HttpError
from src.utils import mime_detector

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

port = int(
    input("Which port do you want to use should be between 5500 and 5600: "))


path = fr"{input('Which path of your computer do you want to share (path should be absolute): ')}"

server = Server(cors=True)

router = server.router()


@router.get('/')
def index(req: HttpRequest, res: HttpResponse):
    index_page_path = os.path.join(os.getcwd(), 'ui', 'dist', 'index.html')

    with open(index_page_path, 'rb') as file:
        mime = mime_detector(file.name)

        res.set_header("Content-Type", mime)

        return file.read()


@router.get('/assets/:file')
def assets(req: HttpRequest, res: HttpResponse):
    asset_path = os.path.join(
        os.getcwd(), 'ui', 'dist', 'assets', req.get_param('file'))

    with open(asset_path, 'rb') as file:
        mime = mime_detector(file.name)

        res.set_header("Content-Type", mime)

        return file.read()


@router.get('/list')
def get_dir_list(req: HttpRequest, res: HttpResponse):
    prefix = req.get_query_param('prefix')

    real_path = path

    if prefix:
        real_path = prefix[0]

    scanner = PathScanner(real_path)

    return scanner.scan()


@router.get('/path')
def get_path(req: HttpRequest, res: HttpResponse):
    return {"path": path}


@router.get('/file')
def send_file(req: HttpRequest, res: HttpResponse):
    path = req.get_query_param('path')

    if not path:
        return {"message": "should feed the url with path query param"}

    path = path[0]

    with open(path, 'rb') as file:
        mime = mime_detector(file.name)

        res.set_header("Content-Type", mime)

        res.set_header(
            "content-disposition", f"attachment; filename={file.name}")

        return file.read()


server.listen(port)
server.start()
