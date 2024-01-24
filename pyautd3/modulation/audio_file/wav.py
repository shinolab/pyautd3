from pathlib import Path

from pyautd3.internal.modulation import IModulationWithSamplingConfig
from pyautd3.internal.utils import _validate_ptr
from pyautd3.native_methods.autd3capi_def import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import (
    NativeMethods as ModulationAudioFile,
)
from pyautd3.sampling_config import SamplingConfiguration


class Wav(IModulationWithSamplingConfig):
    """Modulation constructed from a wav file.

    The data is resampled to the sampling frequency of the Modulation.
    """

    _path: Path

    def __init__(self: "Wav", path: Path) -> None:
        """Constructor.

        Arguments:
        ---------
            path: Path to the wav file
        """
        super().__init__(SamplingConfiguration.from_frequency(4e3))
        self._path = path

    def _modulation_ptr(self: "Wav") -> ModulationPtr:
        return _validate_ptr(
            ModulationAudioFile().modulation_wav(
                str(self._path).encode("utf-8"),
                self._config._internal,
            ),
        )
