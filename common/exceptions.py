from common.baseError import ServerError


class ConfigParseError(ServerError):
    def __init__(self, message: str="Config parse error."):
        super().__init__(message)


class OutOfBounds(ValueError):
    def __init__(self, message: str="Index out of edge."):
        super().__init__(message)


class LeakageOfArgument(ServerError):
    def __init__(self, message: str="Leakage of argument."):
        super().__init__(message)