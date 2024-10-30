from datetime import timedelta
from pathlib import Path
from typing import Self
from pyautd3.derive import datagram
from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.fir import IntoModulationFir
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.modulation.resample import Resampler
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import NativeMethods as ModulationAudioFile
from pyautd3.native_methods.utils import _validate_ptr
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold



class RawPCM(IntoModulationCache[RawPCM], IntoModulationFir[RawPCM], IntoModulationRadiationPressure[RawPCM], ModulationBase[RawPCM]):
    _path: Path
    _config: SamplingConfig | tuple[Freq[float], SamplingConfig, Resampler]
    _sample_rate: Freq[int]
    def __private_init__(self, path: Path, config: SamplingConfig | tuple[Freq[float], SamplingConfig, Resampler]) -> None: ...
    def __init__(self, path: Path, config: SamplingConfig | Freq[int] | Freq[float] | timedelta) -> None: ...
    def _modulation_ptr(self, ) -> ModulationPtr: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[RawPCM]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[RawPCM]: ...
    @staticmethod
    def new_with_resample(path: Path, source: Freq[float], target: SamplingConfig | Freq[int] | Freq[float] | timedelta, resampler: Resampler) -> RawPCM: ...
