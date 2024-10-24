from datetime import timedelta
from pathlib import Path
from typing import Self

from pyautd3 import SamplingConfig
from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.fir import IntoModulationFir
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.defined.freq import Freq
from pyautd3.modulation.resample import Resampler
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import (
    NativeMethods as ModulationAudioFile,
)
from pyautd3.native_methods.utils import _validate_ptr


class Wav(
    IntoModulationCache["Wav"],
    IntoModulationFir["Wav"],
    IntoModulationRadiationPressure["Wav"],
    ModulationBase["Wav"],
):
    _path: Path
    _resampler: tuple[SamplingConfig, Resampler] | None

    def __init__(self: Self, path: Path) -> None:
        super().__init__()
        self._path = path
        self._resampler = None

    @staticmethod
    def new_with_resample(
        path: Path,
        target: SamplingConfig | Freq[int] | Freq[float] | timedelta,
        resampler: Resampler,
    ) -> "Wav":
        instance = Wav(path)
        instance._resampler = (SamplingConfig(target), resampler)
        return instance

    def _modulation_ptr(self: Self) -> ModulationPtr:
        path = str(self._path).encode("utf-8")
        match self._resampler:
            case (SamplingConfig(), Resampler()):
                (target, resampler) = self._resampler  # type: ignore[misc]
                return _validate_ptr(
                    ModulationAudioFile().modulation_audio_file_wav_with_resample(
                        path,
                        self._loop_behavior,
                        target._inner,
                        resampler._dyn_resampler(),
                    ),
                )
            case _:
                return _validate_ptr(
                    ModulationAudioFile().modulation_audio_file_wav(
                        path,
                        self._loop_behavior,
                    ),
                )
