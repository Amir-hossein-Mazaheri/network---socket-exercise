import os
import logging
from pathlib import Path
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

should_server = input("do you want to run as server: ").lower() == 'y'

path = ''

if should_server:
    path = fr"{input('Which path of you computer do you want to share: ')}"

scanner = PathScanner()


@router.get('/get-dir-list')
def get_dir_list(req: HttpRequest):
    scanner.set_path(path)

    return scanner.scan()


@router.get('/path')
def get_path(req: HttpRequest):
    return {"path": path}


@router.put('/path')
def set_path(req: HttpRequest):
    scanner.set_path(req.get_body()['path'])
    return {"path": path}


server = Server(router)

if should_server:
    server.listen(port)
    server.start()
