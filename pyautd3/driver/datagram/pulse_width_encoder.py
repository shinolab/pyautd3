import ctypes
import threading
from collections.abc import Callable

from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.geometry.device import Device
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr

from .datagram import Datagram


class PulseWidthEncoder(
    IntoDatagramWithTimeout["PulseWidthEncoder"],
    IntoDatagramWithParallelThreshold["PulseWidthEncoder"],
    Datagram,
):
    _cache: dict[int, Callable[[int], int]]
    _lock: threading.Lock

    def __init__(self: "PulseWidthEncoder", f: Callable[[Device], Callable[[int], int]] | None = None) -> None:
        super().__init__()
        self._cache = {}
        self._lock = threading.Lock()

        if f is None:
            self._f_native = None
        else:

            def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int, idx: int) -> int:
                if dev_idx not in self._cache:
                    with self._lock:
                        self._cache[dev_idx] = f(Device(dev_idx, Base().device(geometry_ptr, dev_idx)))
                return self._cache[dev_idx](idx)

            self._f_native = ctypes.CFUNCTYPE(ctypes.c_uint16, ctypes.c_void_p, GeometryPtr, ctypes.c_uint16, ctypes.c_uint16)(f_native)

    def _datagram_ptr(self: "PulseWidthEncoder", geometry: Geometry) -> DatagramPtr:
        return (
            Base().datagram_pulse_width_encoder_default()
            if self._f_native is None
            else Base().datagram_pulse_width_encoder(self._f_native, None, geometry._ptr)  # type: ignore[arg-type]
        )
