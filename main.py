import os
import logging
from dotenv import load_dotenv

from src.PathScanner import PathScanner
from src.Server import Server
from src.Router import Router
from src.HttpRequest import HttpRequest

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


load_dotenv()


port = int(os.getenv("PORT", 5000))

router = Router()

path = fr"{input('Which path of your computer do you want to share (path should be absolute): ')}"


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


server = Server(router)

server.listen(port)
server.start()
