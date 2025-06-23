import ctypes
from collections.abc import Callable
from typing import Self

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.ethercat.dc_sys_time import DcSysTime
from pyautd3.native_methods.autd3 import GPIOOut
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr, GPIOOutputTypeWrap
from pyautd3.native_methods.utils import ConstantADT


class GPIOOutputType(metaclass=ConstantADT):
    def __new__(cls: type["GPIOOutputType"]) -> "GPIOOutputType":
        raise NotImplementedError

    BaseSignal: GPIOOutputTypeWrap = Base().gpio_output_type_base_signal()
    Thermo: GPIOOutputTypeWrap = Base().gpio_output_type_thermo()
    ForceFan: GPIOOutputTypeWrap = Base().gpio_output_type_force_fan()
    Sync: GPIOOutputTypeWrap = Base().gpio_output_type_sync()
    ModSegment: GPIOOutputTypeWrap = Base().gpio_output_type_mod_segment()
    SyncDiff: GPIOOutputTypeWrap = Base().gpio_output_type_sync_diff()

    @staticmethod
    def ModIdx(idx: int) -> GPIOOutputTypeWrap:  # noqa: N802
        return Base().gpio_output_type_mod_idx(idx)

    StmSegment: GPIOOutputTypeWrap = Base().gpio_output_type_stm_segment()

    @staticmethod
    def StmIdx(idx: int) -> GPIOOutputTypeWrap:  # noqa: N802
        return Base().gpio_output_type_stm_idx(idx)

    IsStmMode: GPIOOutputTypeWrap = Base().gpio_output_type_is_stm_mode()

    @staticmethod
    def PwmOut(tr: Transducer) -> GPIOOutputTypeWrap:  # noqa: N802
        return Base().gpio_output_type_pwm_out(tr._ptr)

    @staticmethod
    def Direct(value: bool) -> GPIOOutputTypeWrap:  # noqa: N802, FBT001
        return Base().gpio_output_type_direct(value)

    @staticmethod
    def SysTimeEq(value: DcSysTime) -> GPIOOutputTypeWrap:  # noqa: N802
        return Base().gpio_output_type_sys_time_eq(value._inner)


class GPIOOutputs(Datagram):
    def __init__(self: Self, f: Callable[[Device, GPIOOut], GPIOOutputTypeWrap | None]) -> None:
        super().__init__()

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int, gpio: GPIOOut, res) -> None:  # noqa: ANN001
            res[0] = f(Device(dev_idx, geometry_ptr), gpio) or Base().gpio_output_type_none()

        self._f_native = ctypes.CFUNCTYPE(
            None,
            ctypes.c_void_p,
            GeometryPtr,
            ctypes.c_uint32,
            ctypes.c_uint8,
            ctypes.POINTER(GPIOOutputTypeWrap),
        )(f_native)

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return Base().datagram_gpio_outputs(self._f_native, None, geometry._geometry_ptr)  # type: ignore[arg-type]
