import os

from src.types import PathItem, PathItemType


class PathScanner:
    __path = ''
    __list: list[PathItem] = []

    def __init__(self, path: str = None) -> None:
        if not path:
            return

        self.set_path(path)

    def set_path(self, path: str):
        if os.path.isfile(path):
            raise ValueError("You must feed path of a directory not a file.")

        self.__path = path

    def scan(self) -> list[PathItem]:
        self.__list = []

        if not self.__path:
            raise ValueError("should set path at some point.")

        for path_item in os.listdir(self.__path):
            try:
                # just makes sure that hidden directories are not exposed
                if path_item.startswith('.'):
                    continue

                path = os.path.join(self.__path, path_item)

                type = PathItemType.DIR if os.path.isdir(
                    path) else PathItemType.FILE

                self.__list.append({
                    "name": path_item,
                    "path": path,
                    "type": type
                })
            except PermissionError:
                continue

        return self.__list

    def get_list(self) -> list[PathItem]:
        return self.__list

    def get_path(self) -> str:
        return self.__path
