import ctypes
import threading
from pathlib import Path

from pyautd3.native_methods.autd3capi_driver import OptionDuration, ResultLink


class RemoteOption(ctypes.Structure):
    _fields_ = [("timeout", OptionDuration)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RemoteOption) and self._fields_ == other._fields_  # pragma: no cover

    def __hash__(self) -> int:
        return super().__hash__()  # pragma: no cover


class Singleton(type):
    _instances = {}  # type: ignore[var-annotated]
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:  # pragma: no cover
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):
    def init_dll(self, bin_location: Path, bin_prefix: str, bin_ext: str) -> None:
        self.dll = ctypes.CDLL(str(bin_location / f"{bin_prefix}autd3capi_link_remote{bin_ext}"))

        self.dll.AUTDLinkRemote.argtypes = [ctypes.c_char_p, RemoteOption]
        self.dll.AUTDLinkRemote.restype = ResultLink

    def link_remote(self, addr: bytes, option: RemoteOption) -> ResultLink:
        return self.dll.AUTDLinkRemote(addr, option)
