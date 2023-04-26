class HttpRequest:
    __method: str
    __route: str
    __query: dict[str, str]
    __params: dict[str, str] = {}
    __headers: dict[str, str]
    __body: any

    def __init__(self, method: str, route: str, query: dict[str, str], headers: dict[str, str], body: any) -> None:
        self.__method = method
        self.__route = route
        self.__query = query
        self.__headers = headers
        self.__body = body

    def get_method(self):
        return self.__method

    def get_route(self):
        return self.__route

    def get_query(self):
        return self.__query

    def get_query_param(self, key: str):
        return self.__query.get(key)

    def get_params(self):
        return self.__params

    def get_param(self, key: str):
        return self.__params.get(key)

    def add_to_params(self, key: str, value: str):
        self.__params[key] = value

    def get_headers(self):
        return self.__headers

    def get_body(self):
        return self.__body

    def get_header(self, key: str):
        return self.__headers.get(key.lower())

    def __str__(self) -> str:
        return (
            f"method: {self.__method}\n"
            f"route: {self.__route}\n"
            f"query: {self.__query}\n"
            f"headers: {self.__headers}\n"
            f"body: {self.__body}"
        )
