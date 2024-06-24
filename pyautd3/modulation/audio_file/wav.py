from pathlib import Path

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.datagram.modulation.transform import IntoModulationTransform
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import (
    NativeMethods as ModulationAudioFile,
)
from pyautd3.native_methods.utils import _validate_ptr


class Wav(
    IntoModulationCache["Wav"],
    IntoModulationTransform["Wav"],
    IntoModulationRadiationPressure["Wav"],
    ModulationBase["Wav"],
):
    _path: Path

    def __init__(self: "Wav", path: Path) -> None:
        super().__init__()
        self._path = path

    def _modulation_ptr(self: "Wav") -> ModulationPtr:
        return _validate_ptr(
            ModulationAudioFile().modulation_audio_file_wav(
                str(self._path).encode("utf-8"),
                self._loop_behavior,
            ),
        )
