# This file is autogenerated
import threading
import ctypes
import os
from pyautd3.native_methods.structs import Vector3, Quaternion, FfiFuture, LocalFfiFuture, SamplingConfig
from pyautd3.native_methods.autd3capi_driver import LinkBuilderPtr


class LinkSimulatorBuilderPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class ResultLinkSimulatorBuilder(ctypes.Structure):
    _fields_ = [("result", LinkSimulatorBuilderPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultLinkSimulatorBuilder) and self._fields_ == other._fields_ # pragma: no cover
                    


class Singleton(type):
    _instances = {}  # type: ignore
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances: # pragma: no cover
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):

    def init_dll(self, bin_location: str, bin_prefix: str, bin_ext: str):
        try:
            self.dll = ctypes.CDLL(os.path.join(bin_location, f'{bin_prefix}autd3capi_link_simulator{bin_ext}'))
        except Exception:   # pragma: no cover
            return          # pragma: no cover

        self.dll.AUTDLinkSimulator.argtypes = [ctypes.c_char_p] 
        self.dll.AUTDLinkSimulator.restype = ResultLinkSimulatorBuilder

        self.dll.AUTDLinkSimulatorWithTimeout.argtypes = [LinkSimulatorBuilderPtr, ctypes.c_uint64]  # type: ignore 
        self.dll.AUTDLinkSimulatorWithTimeout.restype = LinkSimulatorBuilderPtr

        self.dll.AUTDLinkSimulatorIntoBuilder.argtypes = [LinkSimulatorBuilderPtr]  # type: ignore 
        self.dll.AUTDLinkSimulatorIntoBuilder.restype = LinkBuilderPtr

    def link_simulator(self, addr: bytes) -> ResultLinkSimulatorBuilder:
        return self.dll.AUTDLinkSimulator(addr)

    def link_simulator_with_timeout(self, simulator: LinkSimulatorBuilderPtr, timeout_ns: int) -> LinkSimulatorBuilderPtr:
        return self.dll.AUTDLinkSimulatorWithTimeout(simulator, timeout_ns)

    def link_simulator_into_builder(self, simulator: LinkSimulatorBuilderPtr) -> LinkBuilderPtr:
        return self.dll.AUTDLinkSimulatorIntoBuilder(simulator)
