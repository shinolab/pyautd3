from typing import Self

from pyautd3.native_methods.autd3capi import NativeMethods as Base


class FirmwareInfo:
    info: str

    def __init__(self: Self, info: str) -> None:
        self.info = info

    @staticmethod
    def latest_version() -> str:
        sb = bytes(bytearray(256))
        Base().firmware_latest(sb)
        return sb.decode("utf-8").rstrip(" \t\r\n\0")

    def __str__(self: Self) -> str:
        return self.info
