import ctypes
from collections.abc import Iterable
from datetime import timedelta
from typing import Generic
from typing import Self
from typing import TypeVar
import numpy as np
from numpy.typing import ArrayLike
import pyautd3.driver.datagram.stm.control_point as cp
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
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
from pyautd3.native_methods.autd3capi_driver import FociSTMPtr
from pyautd3.native_methods.autd3capi_driver import Segment
from pyautd3.native_methods.autd3capi_driver import TransitionModeWrap
from pyautd3.native_methods.autd3capi_driver import LoopBehavior as _LoopBehavior
from pyautd3.native_methods.utils import _validate_ptr
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold

C = TypeVar("C", bound=cp.IControlPoints)

class FociSTM(IntoDatagramWithSegment, DatagramS[FociSTMPtr], Datagram, Generic[C]):
    _points: list[C]
    _stm_sampling_config: STMSamplingConfig
    _loop_behavior: _LoopBehavior
    def __private_init__(self, sampling_config: STMSamplingConfig, foci: list[ArrayLike] | list[cp.ControlPoints1] | list[cp.ControlPoints2] | list[cp.ControlPoints3] | list[cp.ControlPoints4] | list[cp.ControlPoints5] | list[cp.ControlPoints6] | list[cp.ControlPoints7] | list[cp.ControlPoints8]) -> None: ...
    def __init__(self, config: SamplingConfig | Freq[float] | timedelta, iterable: Iterable[ArrayLike] | Iterable[cp.ControlPoints1] | Iterable[cp.ControlPoints2] | Iterable[cp.ControlPoints3] | Iterable[cp.ControlPoints4] | Iterable[cp.ControlPoints5] | Iterable[cp.ControlPoints6] | Iterable[cp.ControlPoints7] | Iterable[cp.ControlPoints8]) -> None: ...
    def _raw_ptr(self, _: Geometry) -> FociSTMPtr: ...
    def _ptr(self, ) -> FociSTMPtr: ...
    def _datagram_ptr(self, geometry: Geometry) -> DatagramPtr: ...
    def _into_segment(self, ptr: FociSTMPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr: ...
    def with_loop_behavior(self, value: _LoopBehavior) -> Self: ...
    def _sampling_config_intensity(self, ) -> SamplingConfig: ...
    def _sampling_config_phase(self, ) -> SamplingConfig: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[FociSTM]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[FociSTM]: ...
    @classmethod
    def nearest(cls, config: Freq[float] | timedelta, iterable: Iterable[ArrayLike] | Iterable[cp.ControlPoints1] | Iterable[cp.ControlPoints2] | Iterable[cp.ControlPoints3] | Iterable[cp.ControlPoints4] | Iterable[cp.ControlPoints5] | Iterable[cp.ControlPoints6] | Iterable[cp.ControlPoints7] | Iterable[cp.ControlPoints8]) -> FociSTM: ...
    @property
    def freq(self) -> Freq[float]: ...
    @property
    def period(self) -> timedelta: ...
    @property
    def sampling_config(self) -> SamplingConfig: ...
