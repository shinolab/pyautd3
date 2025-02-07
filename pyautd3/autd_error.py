from typing import Self


class AUTDError(Exception):
    msg: str

    def __init__(self: Self, err: bytes | str) -> None:
        self.msg = err if isinstance(err, str) else err.decode("utf-8").rstrip(" \t\r\n\0")

    def __str__(self: Self) -> str:
        return self.msg

    def __repr__(self: Self) -> str:
        return self.msg


class UnknownGroupKeyError(AUTDError):
    def __init__(self: Self) -> None:
        super().__init__("Unknown group key")


class InvalidDatagramTypeError(AUTDError):
    def __init__(self: Self) -> None:
        super().__init__("Invalid datagram type")


class CantBeZeroError(AUTDError):
    def __init__(self: Self, v: int) -> None:
        super().__init__(f"Value must be greater than 0: {v}")
