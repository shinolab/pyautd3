import ctypes
from collections.abc import Callable

from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr

from .datagram import Datagram


class PhaseFilter(Datagram):
    _f_native: ctypes.CFUNCTYPE(ctypes.c_uint8, ctypes.c_void_p, GeometryPtr, ctypes.c_uint32, ctypes.c_uint8)  # type: ignore[valid-type]

    def __new__(cls: type["PhaseFilter"]) -> "PhaseFilter":
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["PhaseFilter"], f: Callable[[Device], Callable[[Transducer], Phase]]) -> "PhaseFilter":
        ins = super().__new__(cls)

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int, tr_idx: int) -> int:
            dev_ptr = Base().device(geometry_ptr, dev_idx)
            return f(Device(dev_idx, dev_ptr))(Transducer(tr_idx, dev_ptr)).value

        ins._f_native = ctypes.CFUNCTYPE(ctypes.c_uint8, ctypes.c_void_p, GeometryPtr, ctypes.c_uint32, ctypes.c_uint8)(f_native)
        return ins

    @staticmethod
    def additive(f: Callable[[Device], Callable[[Transducer], Phase]]) -> "PhaseFilter":
        return PhaseFilter.__private_new__(f)

    def _datagram_ptr(self: "PhaseFilter", geometry: Geometry) -> DatagramPtr:
        return Base().datagram_phase_filter_additive(self._f_native, None, geometry._ptr)  # type: ignore[arg-type]
