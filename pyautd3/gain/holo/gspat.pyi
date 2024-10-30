import ctypes
from collections.abc import Iterable
from typing import Self
import numpy as np
from pyautd3.derive import builder
from pyautd3.derive import datagram
from pyautd3.derive import gain
from pyautd3.driver.geometry import Geometry
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.gain.holo.backend import Backend
from pyautd3.gain.holo.constraint import EmissionConstraint
from pyautd3.gain.holo.holo import HoloWithBackend
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3
from pyautd3.gain.cache import Cache
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold



class GSPAT(HoloWithBackend[GSPAT]):
    def __init__(self, backend: Backend, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> None: ...
    def _gain_ptr(self, _: Geometry) -> GainPtr: ...
    def with_repeat(self, repeat: int) -> GSPAT: ...
    def with_cache(self, ) -> Cache[GSPAT]: ...
    def with_segment(self, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[GSPAT]: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[GSPAT]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[GSPAT]: ...
    @property
    def repeat(self) -> int: ...
