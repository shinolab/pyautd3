from datetime import timedelta
from pathlib import Path
from typing import Self
from pyautd3 import SamplingConfig
from pyautd3.derive import datagram
from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.fir import IntoModulationFir
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.defined.freq import Freq
from pyautd3.modulation.resample import Resampler
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import NativeMethods as ModulationAudioFile
from pyautd3.native_methods.utils import _validate_ptr
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold



class Wav(IntoModulationCache[Wav], IntoModulationFir[Wav], IntoModulationRadiationPressure[Wav], ModulationBase[Wav]):
    _path: Path
    _resampler: tuple[SamplingConfig, Resampler] | None
    def __init__(self, path: Path) -> None: ...
    def _modulation_ptr(self, ) -> ModulationPtr: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Wav]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Wav]: ...
    @staticmethod
    def new_with_resample(path: Path, target: SamplingConfig | Freq[int] | Freq[float] | timedelta, resampler: Resampler) -> Wav: ...
