import ctypes
from typing import Self

from pyautd3.derive.derive_builder import builder
from pyautd3.native_methods.autd3capi import NativeMethods as Base


@builder
class FirmwareInfo:
    _prop_info: str

    def __init__(self: Self, info: str) -> None:
        self._prop_info = info

    @staticmethod
    def latest_version() -> str:
        sb = ctypes.create_string_buffer(256)
        Base().firmware_latest(sb)
        return sb.value.decode("utf-8")

    def __str__(self: Self) -> str:
        return self._prop_info
