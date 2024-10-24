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


class Csv(
    IntoModulationCache["Csv"],
    IntoModulationFir["Csv"],
    IntoModulationRadiationPressure["Csv"],
    ModulationBase["Csv"],
):
    _path: Path
    _config: SamplingConfig | tuple[Freq[float], SamplingConfig, Resampler]
    _deliminator: str

    def __private_init__(self: Self, path: Path, config: SamplingConfig | tuple[Freq[float], SamplingConfig, Resampler]) -> None:
        super().__init__()
        self._path = path
        self._config = config
        self._deliminator = ","

    def __init__(self: Self, path: Path, config: SamplingConfig | Freq[int] | Freq[float] | timedelta) -> None:
        self.__private_init__(path, SamplingConfig(config))

    @staticmethod
    def new_with_resample(
        path: Path,
        source: Freq[float],
        target: SamplingConfig | Freq[int] | Freq[float] | timedelta,
        resampler: Resampler,
    ) -> "Csv":
        instance = super(Csv, Csv).__new__(Csv)
        instance.__private_init__(path, (source, SamplingConfig(target), resampler))
        return instance

    def with_deliminator(self: Self, deliminator: str) -> Self:
        self._deliminator = deliminator
        return self

    def _modulation_ptr(self: Self) -> ModulationPtr:
        delim = self._deliminator.encode("utf-8")
        path = str(self._path).encode("utf-8")
        match self._config:
            case (Freq(), SamplingConfig(), Resampler()):
                (source, target, resampler) = self._config  # type: ignore[misc]
                return _validate_ptr(
                    ModulationAudioFile().modulation_audio_file_csv_with_resample(
                        path,
                        delim[0],
                        self._loop_behavior,
                        source.hz,
                        target._inner,
                        resampler._dyn_resampler(),
                    ),
                )
            case _:
                return _validate_ptr(
                    ModulationAudioFile().modulation_audio_file_csv(
                        str(self._path).encode("utf-8"),
                        self._config._inner,  # type: ignore[union-attr]
                        delim[0],
                        self._loop_behavior,
                    ),
                )
