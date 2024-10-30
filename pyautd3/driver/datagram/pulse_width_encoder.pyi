from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from collections.abc import Callable
from ctypes import CFUNCTYPE, c_uint8, c_uint16, c_void_p
from threading import Lock
from typing import Self
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.geometry.device import Device
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr
from .datagram import Datagram



class PulseWidthEncoder(Datagram):
    _cache: dict[int, Callable[[int], int]]
    _lock: Lock
    def __init__(self, f: Callable[[Device], Callable[[int], int]] | None = None) -> None: ...
    def _datagram_ptr(self, geometry: Geometry) -> DatagramPtr: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[PulseWidthEncoder]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[PulseWidthEncoder]: ...
