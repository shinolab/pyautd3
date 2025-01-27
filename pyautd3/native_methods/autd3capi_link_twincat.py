import ctypes
import threading
from pathlib import Path

from pyautd3.native_methods.autd3capi_driver import LinkBuilderPtr, ResultLinkBuilder, ResultStatus


class Singleton(type):
    _instances = {}
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
        self.dll.AUTDLinkTwinCAT.restype = LinkBuilderPtr

        self.dll.AUTDLinkRemoteTwinCAT.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.dll.AUTDLinkRemoteTwinCAT.restype = ResultLinkBuilder

    def link_twin_cat_tracing_init(self) -> None:
        return self.dll.AUTDLinkTwinCATTracingInit()

    def link_twin_cat_tracing_init_with_file(self, path: ctypes.Array[ctypes.c_char]) -> ResultStatus:
        return self.dll.AUTDLinkTwinCATTracingInitWithFile(path)

    def link_twin_cat(self) -> LinkBuilderPtr:
        return self.dll.AUTDLinkTwinCAT()

    def link_remote_twin_cat(
        self, server_ams_net_id: ctypes.Array[ctypes.c_char], server_ip: ctypes.Array[ctypes.c_char], client_ams_net_id: ctypes.Array[ctypes.c_char],
    ) -> ResultLinkBuilder:
        return self.dll.AUTDLinkRemoteTwinCAT(server_ams_net_id, server_ip, client_ams_net_id)
