# This file is autogenerated
import threading
import ctypes
import os
from pyautd3.native_methods.structs import Point3, Vector3, Quaternion, FfiFuture, LocalFfiFuture
from pyautd3.native_methods.autd3_driver import SamplingConfig, LoopBehavior, SyncMode, GainSTMMode, GPIOOut, GPIOIn, Segment, SilencerTarget, Drive, DcSysTime
from pyautd3.native_methods.autd3capi_driver import ResultStatus, ResultSyncLinkBuilder



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
        self.dll = ctypes.CDLL(os.path.join(bin_location, f'{bin_prefix}autd3capi_link_simulator{bin_ext}'))

        self.dll.AUTDLinkSimulatorTracingInit.argtypes = [] 
        self.dll.AUTDLinkSimulatorTracingInit.restype = None

        self.dll.AUTDLinkSimulatorTracingInitWithFile.argtypes = [ctypes.c_char_p] 
        self.dll.AUTDLinkSimulatorTracingInitWithFile.restype = ResultStatus

        self.dll.AUTDLinkSimulator.argtypes = [ctypes.c_char_p] 
        self.dll.AUTDLinkSimulator.restype = ResultSyncLinkBuilder

    def link_simulator_tracing_init(self) -> None:
        return self.dll.AUTDLinkSimulatorTracingInit()

    def link_simulator_tracing_init_with_file(self, path: bytes) -> ResultStatus:
        return self.dll.AUTDLinkSimulatorTracingInitWithFile(path)

    def link_simulator(self, addr: bytes) -> ResultSyncLinkBuilder:
        return self.dll.AUTDLinkSimulator(addr)
