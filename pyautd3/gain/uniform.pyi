from pyautd3.gain.cache import Cache
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from typing import Self
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.drive import Drive
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr



class Uniform(Gain):
    _drive: Drive
    def __init__(self, drive: Drive | EmitIntensity | Phase | tuple) -> None: ...
    def _gain_ptr(self, _: Geometry) -> GainPtr: ...
    def with_cache(self, ) -> Cache[Uniform]: ...
    def with_segment(self, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Uniform]: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Uniform]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Uniform]: ...
    @property
    def drive(self) -> Drive: ...
