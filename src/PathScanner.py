import os

from src.types import PathItem, PathItemType


class PathScanner:
    __path = ''
    __list: list[PathItem] = []

    def __init__(self, path: str) -> None:
        if os.path.isfile(path):
            raise ValueError("You must feed path of a directory not a file.")

        self.__path = path

    def scan(self) -> list[PathItem]:
        for path_item in os.listdir(self.__path):
            # just makes sure that hidden directories are not exposed
            if path_item.startswith('.'):
                continue

            type = PathItemType.DIR if os.path.isdir(
                path_item) else PathItemType.FILE

            self.__list.append({
                "name": path_item,
                "path": os.path.join(self.__path, path_item),
                "type": type
            })

        return self.__list

    def get_list(self) -> list[PathItem]:
        return self.__list

    def get_path(self) -> str:
        return self.__path
