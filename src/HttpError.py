class HttpError(Exception):
    msg: str
    status: int
    detail: str

    def __init__(self, status: int, msg: str, detail: str = None) -> None:
        super().__init__(msg)

        self.msg = msg
        self.status = status
        self.detail = detail
