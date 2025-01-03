# This file is autogenerated
import threading
import ctypes
import os
from pyautd3.native_methods.structs import Point3, Vector3, Quaternion, FfiFuture, LocalFfiFuture
from enum import IntEnum


class SyncMode(IntEnum):
    DC = 0
    FreeRun = 1

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class GainSTMMode(IntEnum):
    PhaseIntensityFull = 0
    PhaseFull = 1
    PhaseHalf = 2

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class GPIOOut(IntEnum):
    O0 = 0
    O1 = 1
    O2 = 2
    O3 = 3

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class GPIOIn(IntEnum):
    I0 = 0
    I1 = 1
    I2 = 2
    I3 = 3

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class Segment(IntEnum):
    S0 = 0
    S1 = 1

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class SilencerTarget(IntEnum):
    Intensity = 0
    PulseWidth = 1

    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover


class DcSysTime(ctypes.Structure):
    _fields_ = [("dc_sys_time", ctypes.c_uint64)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DcSysTime) and self._fields_ == other._fields_  # pragma: no cover


class Drive(ctypes.Structure):
    _fields_ = [("phase", ctypes.c_uint8), ("intensity", ctypes.c_uint8)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Drive) and self._fields_ == other._fields_  # pragma: no cover


class LoopBehavior(ctypes.Structure):
    _fields_ = [("rep", ctypes.c_uint16)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LoopBehavior) and self._fields_ == other._fields_  # pragma: no cover


class SamplingConfig(ctypes.Structure):
    _fields_ = [("division", ctypes.c_uint16)]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SamplingConfig) and self._fields_ == other._fields_  # pragma: no cover


