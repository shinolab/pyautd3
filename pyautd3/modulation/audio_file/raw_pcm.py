from pathlib import Path

from pyautd3.driver.common.sampling_config import SamplingConfiguration
from pyautd3.driver.datagram.modulation import IModulationWithSamplingConfig
from pyautd3.native_methods.autd3capi_def import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import (
    NativeMethods as ModulationAudioFile,
)
from pyautd3.native_methods.utils import _validate_ptr


class RawPCM(IModulationWithSamplingConfig):
    """Modulation constructed from a raw PCM data.

    The data must be 8bit unsinged integer.

    The data is resampled to the sampling frequency of the Modulation.
    """

    _path: Path
    _sample_rate: int

    def __init__(self: "RawPCM", path: Path, sample_rate: int) -> None:
        """Constructor.

        Arguments:
        ---------
            path: Path to the raw PCM data
            sample_rate: Sampling frequency of the raw PCM data
        """
        super().__init__(SamplingConfiguration.from_frequency(4e3))
        self._path = path
        self._sample_rate = sample_rate

    def _modulation_ptr(self: "RawPCM") -> ModulationPtr:
        return _validate_ptr(
            ModulationAudioFile().modulation_raw_pcm(
                str(self._path).encode("utf-8"),
                self._sample_rate,
                self._config._internal,
            ),
        )
