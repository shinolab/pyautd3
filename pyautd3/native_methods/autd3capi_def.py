# This file is autogenerated
import threading
import ctypes
import os
from enum import IntEnum

class GainSTMMode(IntEnum):
    PhaseIntensityFull = 0
    PhaseFull = 1
    PhaseHalf = 2

    @classmethod
    def from_param(cls, obj):
        return int(obj)


class Segment(IntEnum):
    S0 = 0
    S1 = 1

    @classmethod
    def from_param(cls, obj):
        return int(obj)


class TimerStrategy(IntEnum):
    Sleep = 0
    BusyWait = 1
    NativeTimer = 2

    @classmethod
    def from_param(cls, obj):
        return int(obj)


class ControllerPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class LinkBuilderPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class LinkPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class DatagramPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class GainPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class GeometryPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class DevicePtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class TransducerPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class ModulationPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class FocusSTMPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class GainSTMPtr(ctypes.Structure):
    _fields_ = [("_0", ctypes.c_void_p)]


class Drive(ctypes.Structure):
    _fields_ = [("phase", ctypes.c_uint8), ("intensity", ctypes.c_uint8)]


class LoopBehavior(ctypes.Structure):
    _fields_ = [("rep", ctypes.c_uint32)]


class ResultI32(ctypes.Structure):
    _fields_ = [("result", ctypes.c_int32), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


class ResultModulation(ctypes.Structure):
    _fields_ = [("result", ModulationPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


class ResultDatagram(ctypes.Structure):
    _fields_ = [("result", DatagramPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


class ResultFocusSTM(ctypes.Structure):
    _fields_ = [("result", FocusSTMPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


class ResultGainSTM(ctypes.Structure):
    _fields_ = [("result", GainSTMPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


class SamplingConfiguration(ctypes.Structure):
    _fields_ = [("div", ctypes.c_uint32)]


class ResultSamplingConfig(ctypes.Structure):
    _fields_ = [("result", SamplingConfiguration), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


class ResultController(ctypes.Structure):
    _fields_ = [("result", ControllerPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]


DEFAULT_CORRECTED_ALPHA: float = 0.803
NUM_TRANS_IN_UNIT: int = 249
NUM_TRANS_IN_X: int = 18
NUM_TRANS_IN_Y: int = 14
TRANS_SPACING_MM: float = 10.16
DEVICE_HEIGHT_MM: float = 151.4
DEVICE_WIDTH_MM: float = 192.0
FPGA_CLK_FREQ: int = 20480000
ULTRASOUND_FREQUENCY: float = 40000.0
AUTD3_ERR: int = -1
AUTD3_TRUE: int = 1
AUTD3_FALSE: int = 0

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
            self.dll = ctypes.CDLL(os.path.join(bin_location, f'{bin_prefix}autd3capi_def{bin_ext}'))
        except Exception:   # pragma: no cover
            return          # pragma: no cover

        self.dll.AUTDEmitIntensityWithCorrectionAlpha.argtypes = [ctypes.c_uint8, ctypes.c_double] 
        self.dll.AUTDEmitIntensityWithCorrectionAlpha.restype = ctypes.c_uint8

        self.dll.AUTDPhaseFromRad.argtypes = [ctypes.c_double] 
        self.dll.AUTDPhaseFromRad.restype = ctypes.c_uint8

        self.dll.AUTDPhaseToRad.argtypes = [ctypes.c_uint8] 
        self.dll.AUTDPhaseToRad.restype = ctypes.c_double

        self.dll.AUTDLoopBehaviorInfinite.argtypes = [] 
        self.dll.AUTDLoopBehaviorInfinite.restype = LoopBehavior

        self.dll.AUTDLoopBehaviorFinite.argtypes = [ctypes.c_uint32] 
        self.dll.AUTDLoopBehaviorFinite.restype = LoopBehavior

        self.dll.AUTDLoopBehaviorOnce.argtypes = [] 
        self.dll.AUTDLoopBehaviorOnce.restype = LoopBehavior

        self.dll.AUTDGetErr.argtypes = [ctypes.c_void_p, ctypes.c_char_p] 
        self.dll.AUTDGetErr.restype = None

        self.dll.AUTDSamplingConfigFromFrequencyDivision.argtypes = [ctypes.c_uint32] 
        self.dll.AUTDSamplingConfigFromFrequencyDivision.restype = ResultSamplingConfig

        self.dll.AUTDSamplingConfigFromFrequency.argtypes = [ctypes.c_double] 
        self.dll.AUTDSamplingConfigFromFrequency.restype = ResultSamplingConfig

        self.dll.AUTDSamplingConfigFromPeriod.argtypes = [ctypes.c_uint64] 
        self.dll.AUTDSamplingConfigFromPeriod.restype = ResultSamplingConfig

        self.dll.AUTDSamplingConfigFrequencyDivision.argtypes = [SamplingConfiguration]  # type: ignore 
        self.dll.AUTDSamplingConfigFrequencyDivision.restype = ctypes.c_uint32

        self.dll.AUTDSamplingConfigFrequency.argtypes = [SamplingConfiguration]  # type: ignore 
        self.dll.AUTDSamplingConfigFrequency.restype = ctypes.c_double

        self.dll.AUTDSamplingConfigPeriod.argtypes = [SamplingConfiguration]  # type: ignore 
        self.dll.AUTDSamplingConfigPeriod.restype = ctypes.c_uint64

    def emit_intensity_with_correction_alpha(self, value: int, alpha: float) -> ctypes.c_uint8:
        return self.dll.AUTDEmitIntensityWithCorrectionAlpha(value, alpha)

    def phase_from_rad(self, value: float) -> ctypes.c_uint8:
        return self.dll.AUTDPhaseFromRad(value)

    def phase_to_rad(self, value: int) -> ctypes.c_double:
        return self.dll.AUTDPhaseToRad(value)

    def loop_behavior_infinite(self) -> LoopBehavior:
        return self.dll.AUTDLoopBehaviorInfinite()

    def loop_behavior_finite(self, v: int) -> LoopBehavior:
        return self.dll.AUTDLoopBehaviorFinite(v)

    def loop_behavior_once(self) -> LoopBehavior:
        return self.dll.AUTDLoopBehaviorOnce()

    def get_err(self, src: ctypes.c_void_p | None, dst: ctypes.Array[ctypes.c_char] | None) -> None:
        return self.dll.AUTDGetErr(src, dst)

    def sampling_config_from_frequency_division(self, div: int) -> ResultSamplingConfig:
        return self.dll.AUTDSamplingConfigFromFrequencyDivision(div)

    def sampling_config_from_frequency(self, f: float) -> ResultSamplingConfig:
        return self.dll.AUTDSamplingConfigFromFrequency(f)

    def sampling_config_from_period(self, p: int) -> ResultSamplingConfig:
        return self.dll.AUTDSamplingConfigFromPeriod(p)

    def sampling_config_frequency_division(self, config: SamplingConfiguration) -> ctypes.c_uint32:
        return self.dll.AUTDSamplingConfigFrequencyDivision(config)

    def sampling_config_frequency(self, config: SamplingConfiguration) -> ctypes.c_double:
        return self.dll.AUTDSamplingConfigFrequency(config)

    def sampling_config_period(self, config: SamplingConfiguration) -> ctypes.c_uint64:
        return self.dll.AUTDSamplingConfigPeriod(config)
