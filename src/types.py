from typing import TypedDict
from enum import Enum


class PathItemType(str, Enum):
    FILE = "FILE"
    DIR = "DIR"


class PathItem(TypedDict):
    name: str
    path: str
    type: PathItemType


class RouterContext(TypedDict):
    filename: str
    download: bool
