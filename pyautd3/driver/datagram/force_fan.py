import ctypes
from collections.abc import Callable

from pyautd3.driver.geometry import Device, Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr, GeometryPtr

from .datagram import Datagram


class ConfigureForceFan(Datagram):
    """Datagram to configure force fan."""

    def __init__(self: "ConfigureForceFan", f: Callable[[Device], bool]) -> None:
        super().__init__()

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int) -> bool:
            return f(Device(dev_idx, Base().device(geometry_ptr, dev_idx)))

        self._f_native = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, GeometryPtr, ctypes.c_uint32)(f_native)

    def _datagram_ptr(self: "ConfigureForceFan", geometry: Geometry) -> DatagramPtr:
        return Base().datagram_configure_force_fan(self._f_native, None, geometry._ptr)  # type: ignore[arg-type]
