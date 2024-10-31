from datetime import timedelta
from pathlib import Path
from typing import Self

from pyautd3.derive import datagram, modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.modulation.resample import Resampler
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import NativeMethods as ModulationAudioFile
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr


@modulation
@datagram_with_segment
@datagram
class RawPCM(Modulation):
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
        path = _to_null_terminated_utf8(str(self._path))
        match self._config:
            case (Freq(), SamplingConfig(), Resampler()):
                (source, target, resampler) = self._config
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
                        _to_null_terminated_utf8(str(self._path)),
                        self._config._inner,
                        self._loop_behavior,
                    ),
                )
