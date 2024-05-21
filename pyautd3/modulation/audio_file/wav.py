from pathlib import Path

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.geometry.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import (
    NativeMethods as ModulationAudioFile,
)
from pyautd3.native_methods.utils import _validate_ptr


class Wav(Modulation["Wav"]):
    _path: Path

    def __init__(self: "Wav", path: Path) -> None:
        super().__init__(SamplingConfig.Division(5120))
        self._path = path

    def _modulation_ptr(self: "Wav", _: Geometry) -> ModulationPtr:
        return _validate_ptr(
            ModulationAudioFile().modulation_wav(
                str(self._path).encode("utf-8"),
                self._config,
                self._loop_behavior,
            ),
        )
