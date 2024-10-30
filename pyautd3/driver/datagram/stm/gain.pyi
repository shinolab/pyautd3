import ctypes
from collections.abc import Iterable
from datetime import timedelta
from typing import Self
import numpy as np
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.datagram.stm.stm_sampling_config import STMSamplingConfig
from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.datagram.with_segment import IntoDatagramWithSegment
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga import LoopBehavior
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_driver import GainSTMMode
from pyautd3.native_methods.autd3capi_driver import GainSTMPtr
from pyautd3.native_methods.autd3capi_driver import Segment
from pyautd3.native_methods.autd3capi_driver import TransitionModeWrap
from pyautd3.native_methods.autd3capi_driver import LoopBehavior as _LoopBehavior
from pyautd3.native_methods.utils import _validate_ptr
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold



class GainSTM(IntoDatagramWithSegment, DatagramS[GainSTMPtr], Datagram):
    _gains: np.ndarray
    _mode: GainSTMMode
    _stm_sampling_config: STMSamplingConfig
    _loop_behavior: _LoopBehavior
    def __private_init__(self, sampling_config: STMSamplingConfig, gains: list[Gain]) -> None: ...
    def __init__(self, config: SamplingConfig | Freq[float] | timedelta, iterable: Iterable[Gain]) -> None: ...
    def _raw_ptr(self, geometry: Geometry) -> GainSTMPtr: ...
    def _ptr(self, gains: np.ndarray) -> GainSTMPtr: ...
    def _datagram_ptr(self, geometry: Geometry) -> DatagramPtr: ...
    def _into_segment(self, ptr: GainSTMPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr: ...
    def with_mode(self, mode: GainSTMMode) -> Self: ...
    def with_loop_behavior(self, value: _LoopBehavior) -> Self: ...
    def _sampling_config_intensity(self, ) -> SamplingConfig: ...
    def _sampling_config_phase(self, ) -> SamplingConfig: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[GainSTM]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[GainSTM]: ...
    @classmethod
    def nearest(cls, config: Freq[float] | timedelta, iterable: Iterable[Gain]) -> GainSTM: ...
    @property
    def mode(self) -> GainSTMMode: ...
    @property
    def freq(self) -> Freq[float]: ...
    @property
    def period(self) -> timedelta: ...
    @property
    def sampling_config(self) -> SamplingConfig: ...
