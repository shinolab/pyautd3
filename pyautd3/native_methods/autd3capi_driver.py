import ctypes
import enum

from pyautd3.native_methods.autd3 import DcSysTime

NUM_TRANS_IN_UNIT: int = 249


NUM_TRANS_IN_X: int = 18


NUM_TRANS_IN_Y: int = 14


TRANS_SPACING_MM: float = 10.16


DEVICE_HEIGHT_MM: float = 151.4


DEVICE_WIDTH_MM: float = 192.0


class DebugTypeTag(enum.IntEnum):
    None_ = 0
    BaseSignal = 1
    Thermo = 2
    ForceFan = 3
    Sync = 4
    ModSegment = 5
    ModIdx = 6
    StmSegment = 7
    StmIdx = 8
    IsStmMode = 9
    PwmOut = 10
    Direct = 11
    SysTimeEq = 12

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class SamplingConfigTag(enum.IntEnum):
    Division = 0
    Frequency = 1
    Period = 2
    FrequencyNearest = 3
    PeriodNearest = 4

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class TransitionModeTag(enum.IntEnum):
    SyncIdx = 0
    SysTime = 1
    Gpio = 2
    Ext = 3
    Immediate = 4
    None_ = 0xFF

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class AUTDStatus(enum.IntEnum):
    AUTDTrue = 0
    AUTDFalse = 1
    AUTDErr = 2

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class SleeperTag(enum.IntEnum):
    Std = 0
    Spin = 1
    Waitable = 3

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class SpinStrategyTag(enum.IntEnum):
    YieldThread = 0
    SpinLoopHint = 1

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class DebugTypeValue(ctypes.Union):
    _fields_ = [("null", ctypes.c_uint64), ("sys_time", DcSysTime), ("idx", ctypes.c_uint16), ("direct", ctypes.c_bool)]


class SamplingConfigValue(ctypes.Union):
    _fields_ = [("division", ctypes.c_uint16), ("freq", ctypes.c_float), ("period_ns", ctypes.c_uint64)]


class TransitionModeValue(ctypes.Union):
    _fields_ = [("null", ctypes.c_uint64), ("sys_time", DcSysTime), ("gpio_in", ctypes.c_uint8)]


class ResultStatus(ctypes.Structure):
    _fields_ = [("result", ctypes.c_uint8), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultStatus) and self._fields_ == other._fields_  # pragma: no cover


class ConstPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ConstPtr) and self._fields_ == other._fields_  # pragma: no cover


class FociSTMPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FociSTMPtr) and self._fields_ == other._fields_  # pragma: no cover


class ResultF32(ctypes.Structure):
    _fields_ = [("result", ctypes.c_float), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultF32) and self._fields_ == other._fields_  # pragma: no cover


class SleeperWrap(ctypes.Structure):
    _fields_ = [("tag", ctypes.c_uint8), ("value", ctypes.c_uint32), ("spin_strategy", ctypes.c_uint8)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SleeperWrap) and self._fields_ == other._fields_  # pragma: no cover


class GeometryPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GeometryPtr) and self._fields_ == other._fields_  # pragma: no cover


class DebugTypeWrap(ctypes.Structure):
    _fields_ = [("ty", ctypes.c_uint8), ("value", DebugTypeValue)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DebugTypeWrap) and self._fields_ == other._fields_  # pragma: no cover


class LinkPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LinkPtr) and self._fields_ == other._fields_  # pragma: no cover


class GainSTMPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GainSTMPtr) and self._fields_ == other._fields_  # pragma: no cover


class SenderPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SenderPtr) and self._fields_ == other._fields_  # pragma: no cover


class TransducerPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TransducerPtr) and self._fields_ == other._fields_  # pragma: no cover


class Duration(ctypes.Structure):
    _fields_ = [("nanos", ctypes.c_uint64)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Duration) and self._fields_ == other._fields_  # pragma: no cover


class TransitionModeWrap(ctypes.Structure):
    _fields_ = [("tag", ctypes.c_uint8), ("value", TransitionModeValue)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TransitionModeWrap) and self._fields_ == other._fields_  # pragma: no cover


class ResultU16(ctypes.Structure):
    _fields_ = [("result", ctypes.c_uint16), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultU16) and self._fields_ == other._fields_  # pragma: no cover


class DatagramPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DatagramPtr) and self._fields_ == other._fields_  # pragma: no cover


class ResultLink(ctypes.Structure):
    _fields_ = [("result", LinkPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultLink) and self._fields_ == other._fields_  # pragma: no cover


class ControllerPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ControllerPtr) and self._fields_ == other._fields_  # pragma: no cover


class SamplingConfigWrap(ctypes.Structure):
    _fields_ = [("tag", ctypes.c_uint8), ("value", SamplingConfigValue)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SamplingConfigWrap) and self._fields_ == other._fields_  # pragma: no cover


class GainPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GainPtr) and self._fields_ == other._fields_  # pragma: no cover


class DevicePtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DevicePtr) and self._fields_ == other._fields_  # pragma: no cover


class OptionDuration(ctypes.Structure):
    _fields_ = [("has_value", ctypes.c_bool), ("value", Duration)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, OptionDuration) and self._fields_ == other._fields_  # pragma: no cover


class LoopBehavior(ctypes.Structure):
    _fields_ = [("rep", ctypes.c_uint16)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LoopBehavior) and self._fields_ == other._fields_  # pragma: no cover


class ModulationPtr(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ModulationPtr) and self._fields_ == other._fields_  # pragma: no cover


class ResultSamplingConfig(ctypes.Structure):
    _fields_ = [("result", SamplingConfigWrap), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultSamplingConfig) and self._fields_ == other._fields_  # pragma: no cover


class ResultDuration(ctypes.Structure):
    _fields_ = [("result", Duration), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultDuration) and self._fields_ == other._fields_  # pragma: no cover


class ResultGain(ctypes.Structure):
    _fields_ = [("result", GainPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultGain) and self._fields_ == other._fields_  # pragma: no cover


class ResultModulation(ctypes.Structure):
    _fields_ = [("result", ModulationPtr), ("err_len", ctypes.c_uint32), ("err", ctypes.c_void_p)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResultModulation) and self._fields_ == other._fields_  # pragma: no cover
