from typing import Generic
from typing import Self
from typing import TypeVar
from pyautd3.derive import datagram
from pyautd3.derive import gain
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import GainCachePtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold

G = TypeVar("G", bound=Gain)

class Cache(Gain, Generic[G]):
    _g: G
    _ptr: GainCachePtr | None
    def __init__(self, g: G) -> None: ...
    def _gain_ptr(self, geometry: Geometry) -> GainPtr: ...
    def __del__(self, ) -> None: ...
    def with_segment(self, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Cache]: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Cache]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Cache]: ...
