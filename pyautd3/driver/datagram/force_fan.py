import ctypes
from collections.abc import Callable
from typing import Self

from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Device, Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr


@datagram
class ForceFan(Datagram):
    def __init__(self: Self, f: Callable[[Device], bool]) -> None:
        super().__init__()

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int) -> bool:
            return f(Device(dev_idx, geometry_ptr))

        self._f_native = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, GeometryPtr, ctypes.c_uint16)(f_native)

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return Base().datagram_force_fan(self._f_native, None, geometry._geometry_ptr)  # type: ignore[arg-type]
