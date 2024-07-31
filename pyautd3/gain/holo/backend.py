from abc import ABCMeta, abstractmethod
from ctypes import Array, c_float

from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import BackendPtr, EmissionConstraintWrap
from pyautd3.native_methods.structs import Vector3


class Backend(metaclass=ABCMeta):
    _ptr: BackendPtr

    def __init__(self: "Backend", ptr: BackendPtr) -> None:
        self._ptr = ptr

    def _backend_ptr(self: "Backend") -> BackendPtr:
        return self._ptr

    @abstractmethod
    def _gs(self: "Backend", foci: Array[Vector3], amps: Array[c_float], size: int, repeat: int, constraint: EmissionConstraintWrap) -> GainPtr:
        pass

    @abstractmethod
    def _gspat(self: "Backend", foci: Array[Vector3], amps: Array[c_float], size: int, repeat: int, constraint: EmissionConstraintWrap) -> GainPtr:
        pass

    @abstractmethod
    def _naive(self: "Backend", foci: Array[Vector3], amps: Array[c_float], size: int, constraint: EmissionConstraintWrap) -> GainPtr:
        pass

    @abstractmethod
    def _lm(
        self: "Backend",
        foci: Array[Vector3],
        amps: Array[c_float],
        size: int,
        eps1: float,
        eps2: float,
        tau: float,
        kmax: int,
        initial: Array[c_float],
        initial_size: int,
        constraint: EmissionConstraintWrap,
    ) -> GainPtr:
        pass
