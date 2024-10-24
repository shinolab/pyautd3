import ctypes
from collections.abc import Callable
from typing import Self

from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.ethercat.dc_sys_time import DcSysTime
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, DebugTypeWrap, GeometryPtr, GPIOOut
from pyautd3.native_methods.utils import ConstantADT

from .datagram import Datagram

__all__ = ["DebugType"]


class DebugType(metaclass=ConstantADT):
    def __new__(cls: type["DebugType"]) -> "DebugType":
        raise NotImplementedError

    NONE: DebugTypeWrap = Base().debug_type_none()
    BaseSignal: DebugTypeWrap = Base().debug_type_base_signal()
    Thermo: DebugTypeWrap = Base().debug_type_thermo()
    ForceFan: DebugTypeWrap = Base().debug_type_force_fan()
    Sync: DebugTypeWrap = Base().debug_type_sync()
    ModSegment: DebugTypeWrap = Base().debug_type_mod_segment()

    @staticmethod
    def ModIdx(idx: int) -> DebugTypeWrap:  # noqa: N802
        return Base().debug_type_mod_idx(idx)

    StmSegment: DebugTypeWrap = Base().debug_type_stm_segment()

    @staticmethod
    def StmIdx(idx: int) -> DebugTypeWrap:  # noqa: N802
        return Base().debug_type_stm_idx(idx)

    IsStmMode: DebugTypeWrap = Base().debug_type_is_stm_mode()

    @staticmethod
    def PwmOut(tr: Transducer) -> DebugTypeWrap:  # noqa: N802
        return Base().debug_type_pwm_out(tr._ptr)

    @staticmethod
    def Direct(value: bool) -> DebugTypeWrap:  # noqa: N802, FBT001
        return Base().debug_type_direct(value)

    @staticmethod
    def SysTimeEq(value: DcSysTime) -> DebugTypeWrap:  # noqa: N802
        return Base().debug_type_sys_time_eq(value.sys_time)


class DebugSettings(
    IntoDatagramWithTimeout["DebugSettings"],
    IntoDatagramWithParallelThreshold["DebugSettings"],
    Datagram,
):
    def __init__(self: Self, f: Callable[[Device, GPIOOut], DebugTypeWrap]) -> None:
        super().__init__()

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int, gpio: GPIOOut, res) -> None:  # noqa: ANN001
            res[0] = f(Device(dev_idx, geometry_ptr), gpio)

        self._f_native = ctypes.CFUNCTYPE(
            None,
            ctypes.c_void_p,
            GeometryPtr,
            ctypes.c_uint32,
            ctypes.c_uint8,
            ctypes.POINTER(DebugTypeWrap),
        )(f_native)

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return Base().datagram_debug_settings(self._f_native, None, geometry._ptr)  # type: ignore[arg-type]
