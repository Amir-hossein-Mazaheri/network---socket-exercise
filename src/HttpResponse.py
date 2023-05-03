class HttpResponse:
    __headers: dict[str, str] = {}
    __context: dict[str, str] = {}
    __status = 200

    def __init__(self) -> None:
        self.__headers["Content-Type"] = "application/json"

    def get_headers(self):
        return self.__headers

    def get_context(self):
        return self.__context

    def get_context_by_key(self, key: str):
        return self.__context.get(key)

    def append_context(self, key: str, value: str):
        self.__context[key] = value

    def set_header(self, key: str, value: str):
        self.__headers[key] = value

    def status(self, status: int):
        self.__status = status

    def get_status(self):
        return self.__status
