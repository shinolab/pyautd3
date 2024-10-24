import ctypes
from typing import Self

from pyautd3.native_methods.autd3capi import NativeMethods as Base


class FirmwareInfo:
    _info: str

    def __init__(self: Self, info: str) -> None:
        self._info = info

    @property
    def info(self: Self) -> str:
        return self._info

    @staticmethod
    def latest_version() -> str:
        sb = ctypes.create_string_buffer(256)
        Base().firmware_latest(sb)
        return sb.value.decode("utf-8")

    def __str__(self: Self) -> str:
        return self._info
