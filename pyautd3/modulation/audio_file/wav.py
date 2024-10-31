from datetime import timedelta
from pathlib import Path
from typing import Self

from pyautd3 import SamplingConfig
from pyautd3.derive import datagram, modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.modulation.resample import Resampler
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import NativeMethods as ModulationAudioFile
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr


@modulation
@datagram
@datagram_with_segment
class Wav(Modulation):
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
        path = _to_null_terminated_utf8(str(self._path))
        match self._resampler:
            case (SamplingConfig(), Resampler()):
                (target, resampler) = self._resampler
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
