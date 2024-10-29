from pyautd3.gain.cache import Cache
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from collections.abc import Callable
from typing import Self
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga import Drive
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3_driver import Drive as _Drive
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ConstPtr, GainPtr, GeometryPtr



class Custom(Gain):
    def __init__(self, f: Callable[[Device], Callable[[Transducer], Drive | EmitIntensity | Phase | tuple]]) -> None: ...
    def _gain_ptr(self, geometry: Geometry) -> GainPtr: ...
    def with_cache(self, ) -> Cache[Custom]: ...
    def with_segment(self, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Custom]: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Custom]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Custom]: ...
