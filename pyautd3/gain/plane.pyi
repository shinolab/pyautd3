from typing import Self
import numpy as np
from numpy.typing import ArrayLike
from pyautd3.derive import builder
from pyautd3.derive import datagram
from pyautd3.derive import gain
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3
from pyautd3.gain.cache import Cache
from pyautd3.native_methods.autd3capi_driver import Segment, TransitionModeWrap
from pyautd3.driver.datagram.with_segment import DatagramWithSegment
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold



class Plane(Gain):
    def __init__(self, direction: ArrayLike) -> None: ...
    def _gain_ptr(self, _: Geometry) -> GainPtr: ...
    def with_intensity(self, intensity: int | EmitIntensity) -> Plane: ...
    def with_phase_offset(self, phase_offset: int | Phase) -> Plane: ...
    def with_cache(self, ) -> Cache[Plane]: ...
    def with_segment(self, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[Plane]: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Plane]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Plane]: ...
    @property
    def dir(self) -> np.ndarray: ...
    @property
    def intensity(self) -> EmitIntensity: ...
    @property
    def phase_offset(self) -> Phase: ...
