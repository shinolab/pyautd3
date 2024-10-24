from datetime import timedelta
from pathlib import Path
from typing import Self

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.fir import IntoModulationFir
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.modulation.resample import Resampler
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import (
    NativeMethods as ModulationAudioFile,
)
from pyautd3.native_methods.utils import _validate_ptr


class RawPCM(
    IntoModulationCache["RawPCM"],
    IntoModulationFir["RawPCM"],
    IntoModulationRadiationPressure["RawPCM"],
    ModulationBase["RawPCM"],
):
    _path: Path
    _config: SamplingConfig | tuple[Freq[float], SamplingConfig, Resampler]
    _sample_rate: Freq[int]

    def __private_init__(self: Self, path: Path, config: SamplingConfig | tuple[Freq[float], SamplingConfig, Resampler]) -> None:
        super().__init__()
        self._path = path
        self._config = config

    def __init__(self: Self, path: Path, config: SamplingConfig | Freq[int] | Freq[float] | timedelta) -> None:
        self.__private_init__(path, SamplingConfig(config))

    @staticmethod
    def new_with_resample(
        path: Path,
        source: Freq[float],
        target: SamplingConfig | Freq[int] | Freq[float] | timedelta,
        resampler: Resampler,
    ) -> "RawPCM":
        instance = super(RawPCM, RawPCM).__new__(RawPCM)
        instance.__private_init__(path, (source, SamplingConfig(target), resampler))
        return instance

    def _modulation_ptr(self: Self) -> ModulationPtr:
        path = str(self._path).encode("utf-8")
        match self._config:
            case (Freq(), SamplingConfig(), Resampler()):
                (source, target, resampler) = self._config  # type: ignore[misc]
                return _validate_ptr(
                    ModulationAudioFile().modulation_audio_file_raw_pcm_with_resample(
                        path,
                        self._loop_behavior,
                        source.hz,
                        target._inner,
                        resampler._dyn_resampler(),
                    ),
                )
            case _:
                return _validate_ptr(
                    ModulationAudioFile().modulation_audio_file_raw_pcm(
                        str(self._path).encode("utf-8"),
                        self._config._inner,  # type: ignore[union-attr]
                        self._loop_behavior,
                    ),
                )
