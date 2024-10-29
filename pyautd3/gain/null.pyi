from pyautd3.gain.cache import Cache
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from typing import Self
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr



class Null(Gain):
    def __init__(self, ) -> None: ...
    def _gain_ptr(self, _: Geometry) -> GainPtr: ...
    def with_cache(self, ) -> Cache[Null]: ...
    def with_segment(self, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Null]: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Null]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Null]: ...
