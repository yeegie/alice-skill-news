from loguru import logger


class DeleteException(Exception):
    def __init__(self, message: str, extra_info):
        super().__init__(message)
        self.extra_info = extra_info

class NotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class ServerError(Exception):
    def __init__(self):
        super().__init__('[500] Server error')
