from pathlib import Path
from typing import Self

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import NativeMethods as ModulationAudioFile
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr


class Wav(Modulation):
    path: Path

    def __init__(self: Self, path: Path) -> None:
        super().__init__()
        self.path = path

    def _modulation_ptr(self: Self) -> ModulationPtr:
        path = _to_null_terminated_utf8(str(self.path))
        return _validate_ptr(ModulationAudioFile().modulation_audio_file_wav(path))
