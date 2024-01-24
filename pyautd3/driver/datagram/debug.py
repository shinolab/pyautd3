import ctypes
from collections.abc import Callable

from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr, GeometryPtr

from .datagram import Datagram


class ConfigureDebugOutputIdx(Datagram):
    """Datagram to configure debug output index."""

    def __init__(self: "ConfigureDebugOutputIdx", f: Callable[[Device], Transducer | None]) -> None:
        super().__init__()

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int) -> int:
            tr = f(Device(dev_idx, Base().device(geometry_ptr, dev_idx)))
            return tr.idx if tr is not None else 0xFF

        self._f_native = ctypes.CFUNCTYPE(ctypes.c_uint8, ctypes.c_void_p, GeometryPtr, ctypes.c_uint32)(f_native)

    def _datagram_ptr(self: "ConfigureDebugOutputIdx", geometry: Geometry) -> DatagramPtr:
        return Base().datagram_configure_debug_output_idx(self._f_native, None, geometry._ptr)  # type: ignore[arg-type]
