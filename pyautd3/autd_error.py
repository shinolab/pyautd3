import ctypes


class AUTDError(Exception):
    msg: str

    def __init__(self: "AUTDError", err: ctypes.Array[ctypes.c_char] | str) -> None:
        self.msg = err if isinstance(err, str) else err.value.decode("utf-8")

    def __str__(self: "AUTDError") -> str:
        return self.msg

    def __repr__(self: "AUTDError") -> str:
        return self.msg


class UnknownGroupKeyError(AUTDError):
    def __init__(self: "UnknownGroupKeyError") -> None:
        super().__init__("Unknown group key")


class KeyAlreadyExistsError(AUTDError):
    def __init__(self: "KeyAlreadyExistsError") -> None:
        super().__init__("Key already exists")


class InvalidDatagramTypeError(AUTDError):
    def __init__(self: "InvalidDatagramTypeError") -> None:
        super().__init__("Invalid datagram type")


class CantBeZeroError(AUTDError):
    def __init__(self: "CantBeZeroError", v: int) -> None:
        super().__init__(f"Value must be greater than 0: {v}")
