from abc import ABCMeta, abstractmethod
from ctypes import Array, c_float
from typing import Self

from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import BackendPtr, GSOption, GSPATOption, LMOption, NaiveOption
from pyautd3.native_methods.structs import Point3


class Backend(metaclass=ABCMeta):
    _ptr: BackendPtr

    def __init__(self: Self, ptr: BackendPtr) -> None:
        self._ptr = ptr

    def _backend_ptr(self: Self) -> BackendPtr:
        return self._ptr

    @abstractmethod
    def _gs(self: Self, foci: Array[Point3], amps: Array[c_float], size: int, option: GSOption) -> GainPtr:
        pass

    @abstractmethod
    def _gspat(self: Self, foci: Array[Point3], amps: Array[c_float], size: int, option: GSPATOption) -> GainPtr:
        pass

    @abstractmethod
    def _naive(self: Self, foci: Array[Point3], amps: Array[c_float], size: int, option: NaiveOption) -> GainPtr:
        pass

    @abstractmethod
    def _lm(self: Self, foci: Array[Point3], amps: Array[c_float], size: int, option: LMOption) -> GainPtr:
        pass
