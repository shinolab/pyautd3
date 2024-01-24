import ctypes
from collections.abc import Callable

from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr, GeometryPtr

from .datagram import Datagram


class ConfigureModDelay(Datagram):
    """Datagram to configure modulation delay."""

    def __init__(self: "ConfigureModDelay", f: Callable[[Device, Transducer], int]) -> None:
        super().__init__()

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int, tr_idx: int) -> int:
            dev = Device(dev_idx, Base().device(geometry_ptr, dev_idx))
            tr = Transducer(tr_idx, dev._ptr)
            return f(dev, tr)

        self._f_native = ctypes.CFUNCTYPE(ctypes.c_uint16, ctypes.c_void_p, GeometryPtr, ctypes.c_uint32, ctypes.c_uint8)(f_native)

    def _datagram_ptr(self: "ConfigureModDelay", geometry: Geometry) -> DatagramPtr:
        return Base().datagram_configure_mod_delay(self._f_native, None, geometry._ptr)  # type: ignore[arg-type]
