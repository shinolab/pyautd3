from typing import Self
from pyautd3.derive import datagram
from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.fir import IntoModulationFir
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.utils import _validate_u8
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold



class Static(IntoModulationCache[Static], IntoModulationFir[Static], IntoModulationRadiationPressure[Static], ModulationBase[Static]):
    _intensity: int
    def __init__(self, intensity: int | None = None) -> None: ...
    def _modulation_ptr(self, ) -> ModulationPtr: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Static]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Static]: ...
    @staticmethod
    def with_intensity(intensity: int) -> Static: ...
    @property
    def intensity(self) -> int: ...
