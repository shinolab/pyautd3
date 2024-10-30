from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from collections.abc import Iterable
from datetime import timedelta
from typing import Self
import numpy as np
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.modulation.resample import Resampler
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr



class Custom(Modulation[Custom]):
    _buf: np.ndarray
    _resampler: tuple[Freq[float], SamplingConfig, Resampler] | None
    def __init__(self, buf: Iterable[int], config: SamplingConfig | Freq[int] | Freq[float] | timedelta) -> None: ...
    def _modulation_ptr(self, ) -> ModulationPtr: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Custom]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Custom]: ...
    @staticmethod
    def new_with_resample(buf: Iterable[int], source: Freq[float], target: SamplingConfig | Freq[int] | Freq[float] | timedelta, resampler: Resampler) -> Custom: ...
