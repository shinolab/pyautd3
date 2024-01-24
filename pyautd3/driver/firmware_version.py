import ctypes

from pyautd3.native_methods.autd3capi import NativeMethods as Base


class FirmwareInfo:
    """Firmware information."""

    _info: str

    def __init__(self: "FirmwareInfo", info: str) -> None:
        self._info = info

    @property
    def info(self: "FirmwareInfo") -> str:
        """Get firmware information."""
        return self._info

    @staticmethod
    def latest_version() -> str:
        """Get latest firmware version."""
        sb = ctypes.create_string_buffer(256)
        Base().firmware_latest(sb)
        return sb.value.decode("utf-8")

    def __str__(self: "FirmwareInfo") -> str:
        return self._info
