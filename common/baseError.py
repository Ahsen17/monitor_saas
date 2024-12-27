class ServerError(Exception):
    def __init__(self, message: str="Internal server error."):
        super().__init__(message)