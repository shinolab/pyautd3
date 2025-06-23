import ctypes
import threading
from pathlib import Path

from pyautd3.native_methods.autd3capi_driver import ResultLink


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
        self.dll = ctypes.CDLL(str(bin_location / f"{bin_prefix}autd3capi_link_simulator{bin_ext}"))

        self.dll.AUTDLinkSimulator.argtypes = [ctypes.c_char_p]
        self.dll.AUTDLinkSimulator.restype = ResultLink

    def link_simulator(self, addr: bytes) -> ResultLink:
        return self.dll.AUTDLinkSimulator(addr)
