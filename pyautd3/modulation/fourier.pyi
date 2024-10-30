from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from collections.abc import Iterable
from typing import Self
from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.fir import IntoModulationFir
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from .sine import Sine



class Fourier(IntoModulationCache[Fourier], IntoModulationFir[Fourier], IntoModulationRadiationPressure[Fourier], ModulationBase[Fourier]):
    _components: list[Sine]
    def __init__(self, iterable: Iterable[Sine]) -> None: ...
    def _modulation_ptr(self, ) -> ModulationPtr: ...
    def with_clamp(self, clamp: bool) -> Fourier: ...
    def with_scale_factor(self, scale_factor: float | None) -> Fourier: ...
    def with_offset(self, offset: int) -> Fourier: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Fourier]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Fourier]: ...
    @property
    def clamp(self) -> bool: ...
    @property
    def scale_factor(self) -> float | None: ...
    @property
    def offset(self) -> int: ...
