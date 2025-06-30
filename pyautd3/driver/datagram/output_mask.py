from collections.abc import Callable
from ctypes import CFUNCTYPE, c_bool, c_uint8, c_uint16, c_void_p
from threading import Lock
from typing import Self

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.geometry.device import Device
from pyautd3.driver.geometry.transducer import Transducer
from pyautd3.native_methods.autd3 import Segment
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr, TransitionModeWrap


class OutputMask(DatagramS[GeometryPtr], Datagram):
    _cache: dict[int, Callable[[Transducer], bool]]
    _lock: Lock

    def __init__(self: Self, f: Callable[[Device], Callable[[Transducer], bool]]) -> None:
        super().__init__()
        self._cache = {}
        self._lock = Lock()

        def f_native(_context: c_void_p, geometry_ptr: GeometryPtr, dev_idx: int, tr_idx: int) -> int:
            if dev_idx not in self._cache:
                with self._lock:
                    self._cache[dev_idx] = f(Device(dev_idx, geometry_ptr))
            return self._cache[dev_idx](Transducer(tr_idx, dev_idx, Base().device(geometry_ptr, dev_idx)))

        self._f_native = CFUNCTYPE(c_bool, c_void_p, GeometryPtr, c_uint16, c_uint8)(f_native)

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return Base().datagram_output_mask(self._f_native, None, geometry._geometry_ptr)  # type: ignore[arg-type]

    def _raw_ptr(self: Self, geometry: Geometry) -> GeometryPtr:
        return geometry._geometry_ptr

    def _into_segment(self: Self, ptr: GeometryPtr, segment: Segment, _transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        return Base().datagram_output_mask_with_segment(self._f_native, None, ptr, segment)  # type: ignore[arg-type]
