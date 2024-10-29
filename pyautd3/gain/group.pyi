from pyautd3.gain.cache import Cache
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from collections.abc import Callable
from ctypes import POINTER, c_int32, c_uint16
from typing import Generic, Self, TypeVar
import numpy as np
from pyautd3.autd_error import UnknownGroupKeyError
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr

K = TypeVar("K")

class Group(Gain, Generic[K]):
    _map: dict[K, Gain]
    _f: Callable[[Device], Callable[[Transducer], K | None]]
    def __init__(self, f: Callable[[Device], Callable[[Transducer], K | None]]) -> None: ...
    def set(self, key: K, gain: Gain) -> Self: ...
    def _gain_ptr(self, geometry: Geometry) -> GainPtr: ...
    def with_cache(self, ) -> Cache[Group]: ...
    def with_segment(self, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Group]: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Group]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Group]: ...
