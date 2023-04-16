class HttpRequest:
    __method: str
    __headers: dict[str, str]
    __body: any

    def __init__(self, method: str, headers: dict[str, str], body: any) -> None:
        self.__method = method
        self.__headers = headers
        self.__body = body

    def get_method(self):
        return self.__method

    def get_headers(self):
        return self.__headers

    def get_body(self):
        return self.__body

    def get_header(self, key: str):
        return self.__headers.get(key.lower())

    def __str__(self) -> str:
        return (
            f"method: {self.__method}\n"
            f"headers: {self.__headers}\n"
            f"body: {self.__body}"
        )
