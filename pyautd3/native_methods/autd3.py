import ctypes
import enum

from pyautd3.native_methods.structs import Point3


class ParallelMode(enum.IntEnum):
    Auto = 0
    On = 1
    Off = 2

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class GPIOOut(enum.IntEnum):
    O0 = 0
    O1 = 1
    O2 = 2
    O3 = 3

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class GPIOIn(enum.IntEnum):
    I0 = 0
    I1 = 1
    I2 = 2
    I3 = 3

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class Segment(enum.IntEnum):
    S0 = 0
    S1 = 1

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class GainSTMMode(enum.IntEnum):
    PhaseIntensityFull = 0
    PhaseFull = 1
    PhaseHalf = 2

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class SilencerTarget(enum.IntEnum):
    Intensity = 0
    PulseWidth = 1

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class DcSysTime(ctypes.Structure):
    _fields_ = [("dc_sys_time", ctypes.c_uint64)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DcSysTime) and self._fields_ == other._fields_  # pragma: no cover


class Phase(ctypes.Structure):
    _fields_ = [("value", ctypes.c_uint8)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Phase) and self._fields_ == other._fields_  # pragma: no cover


class EmitIntensity(ctypes.Structure):
    _fields_ = [("value", ctypes.c_uint8)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EmitIntensity) and self._fields_ == other._fields_  # pragma: no cover


class FixedCompletionSteps(ctypes.Structure):
    _fields_ = [("intensity", ctypes.c_uint16), ("phase", ctypes.c_uint16), ("strict_mode", ctypes.c_bool)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FixedCompletionSteps) and self._fields_ == other._fields_  # pragma: no cover


class FixedUpdateRate(ctypes.Structure):
    _fields_ = [("intensity", ctypes.c_uint16), ("phase", ctypes.c_uint16)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FixedUpdateRate) and self._fields_ == other._fields_  # pragma: no cover


class FocusOption(ctypes.Structure):
    _fields_ = [("intensity", EmitIntensity), ("phase_offset", Phase)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FocusOption) and self._fields_ == other._fields_  # pragma: no cover


class GainSTMOption(ctypes.Structure):
    _fields_ = [("mode", ctypes.c_uint8)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GainSTMOption) and self._fields_ == other._fields_  # pragma: no cover


class BesselOption(ctypes.Structure):
    _fields_ = [("intensity", EmitIntensity), ("phase_offset", Phase)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BesselOption) and self._fields_ == other._fields_  # pragma: no cover


class FPGAState(ctypes.Structure):
    _fields_ = [("state", ctypes.c_uint8)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FPGAState) and self._fields_ == other._fields_  # pragma: no cover


class Angle(ctypes.Structure):
    _fields_ = [("radian", ctypes.c_float)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Angle) and self._fields_ == other._fields_  # pragma: no cover


class PlaneOption(ctypes.Structure):
    _fields_ = [("intensity", EmitIntensity), ("phase_offset", Phase)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PlaneOption) and self._fields_ == other._fields_  # pragma: no cover


class Drive(ctypes.Structure):
    _fields_ = [("phase", Phase), ("intensity", EmitIntensity)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Drive) and self._fields_ == other._fields_  # pragma: no cover


class ControlPoint(ctypes.Structure):
    _fields_ = [("point", Point3), ("phase_offset", Phase)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ControlPoint) and self._fields_ == other._fields_  # pragma: no cover
