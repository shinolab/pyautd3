from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from typing import Self, TypeVar
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq, Hz
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.modulation.sampling_mode import ISamplingMode, SamplingModeExact, SamplingModeExactFloat, SamplingModeNearest
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

T = TypeVar("T", int, float)

class Square(Modulation[Square]):
    _mode: ISamplingMode
    def __private__init__(self, mode: ISamplingMode) -> None: ...
    def __init__(self, freq: Freq[T]) -> None: ...
    def _modulation_ptr(self, ) -> ModulationPtr: ...
    def with_low(self, low: int) -> Square: ...
    def with_high(self, high: int) -> Square: ...
    def with_duty(self, duty: float) -> Square: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Square]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Square]: ...
    @classmethod
    def nearest(cls, freq: Freq[float]) -> Square: ...
    @property
    def freq(self) -> Freq[int] | Freq[float]: ...
    @property
    def low(self) -> int: ...
    @property
    def high(self) -> int: ...
    @property
    def duty(self) -> float: ...
