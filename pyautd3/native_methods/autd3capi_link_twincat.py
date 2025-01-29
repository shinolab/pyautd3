import ctypes
import threading
from pathlib import Path

from pyautd3.native_methods.autd3capi_driver import ResultLink, ResultStatus


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
        self.dll = ctypes.CDLL(str(bin_location / f"{bin_prefix}autd3capi_link_twincat{bin_ext}"))

        self.dll.AUTDLinkTwinCATTracingInit.argtypes = []
        self.dll.AUTDLinkTwinCATTracingInit.restype = None

        self.dll.AUTDLinkTwinCATTracingInitWithFile.argtypes = [ctypes.c_char_p]
        self.dll.AUTDLinkTwinCATTracingInitWithFile.restype = ResultStatus

        self.dll.AUTDLinkTwinCAT.argtypes = []
        self.dll.AUTDLinkTwinCAT.restype = ResultLink

        self.dll.AUTDLinkRemoteTwinCAT.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.dll.AUTDLinkRemoteTwinCAT.restype = ResultLink

    def link_twin_cat_tracing_init(self) -> None:
        return self.dll.AUTDLinkTwinCATTracingInit()

    def link_twin_cat_tracing_init_with_file(self, path: bytes) -> ResultStatus:
        return self.dll.AUTDLinkTwinCATTracingInitWithFile(path)

    def link_twin_cat(self) -> ResultLink:
        return self.dll.AUTDLinkTwinCAT()

    def link_remote_twin_cat(self, server_ams_net_id: bytes, server_ip: bytes, client_ams_net_id: bytes) -> ResultLink:
        return self.dll.AUTDLinkRemoteTwinCAT(server_ams_net_id, server_ip, client_ams_net_id)
