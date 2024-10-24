import ctypes
import threading
from collections.abc import Callable
from typing import Self

from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.geometry.device import Device
from pyautd3.driver.geometry.transducer import Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr

from .datagram import Datagram


class PhaseCorrection(
    IntoDatagramWithTimeout["PhaseCorrection"],
    IntoDatagramWithParallelThreshold["PhaseCorrection"],
    Datagram,
):
    _cache: dict[int, Callable[[Transducer], Phase]]
    _lock: threading.Lock

    def __init__(self: Self, f: Callable[[Device], Callable[[Transducer], Phase]]) -> None:
        super().__init__()
        self._cache = {}
        self._lock = threading.Lock()

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int, tr_idx: int) -> int:
            if dev_idx not in self._cache:
                with self._lock:
                    self._cache[dev_idx] = f(Device(dev_idx, geometry_ptr))
            return self._cache[dev_idx](Transducer(tr_idx, dev_idx, Base().device(geometry_ptr, dev_idx))).value

        self._f_native = ctypes.CFUNCTYPE(ctypes.c_uint8, ctypes.c_void_p, GeometryPtr, ctypes.c_uint16, ctypes.c_uint8)(f_native)

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return Base().datagram_phase_corr(self._f_native, None, geometry._ptr)  # type: ignore[arg-type]
