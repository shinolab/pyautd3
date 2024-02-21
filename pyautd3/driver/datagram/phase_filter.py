import ctypes
from collections.abc import Callable

from pyautd3.driver.common import Phase
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr, GeometryPtr

from .datagram import Datagram


class ConfigurePhaseFilter(Datagram):
    """Datagram to configure phase filter."""

    def __init__(self: "ConfigurePhaseFilter", f: Callable[[Device, Transducer], Phase]) -> None:
        super().__init__()

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int, tr_idx: int) -> int:
            dev_ptr = Base().device(geometry_ptr, dev_idx)
            return f(Device(dev_idx, dev_ptr), Transducer(tr_idx, dev_ptr)).value

        self._f_native = ctypes.CFUNCTYPE(ctypes.c_uint8, ctypes.c_void_p, GeometryPtr, ctypes.c_uint32, ctypes.c_uint8)(f_native)

    def _datagram_ptr(self: "ConfigurePhaseFilter", geometry: Geometry) -> DatagramPtr:
        return Base().datagram_configure_phase_filter(self._f_native, None, geometry._ptr)  # type: ignore[arg-type]
