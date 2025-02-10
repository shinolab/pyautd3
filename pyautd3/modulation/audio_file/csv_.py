from pathlib import Path
from typing import Self

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import NativeMethods as ModulationAudioFile
from pyautd3.native_methods.utils import _to_null_terminated_utf8, _validate_ptr
from pyautd3.utils import Duration


class CsvOption:
    delimiter: str

    def __init__(self: Self, *, delimiter: str = ",") -> None:
        self.delimiter = delimiter


class Csv(Modulation):
    path: Path
    config: SamplingConfig | Freq[int] | Freq[float] | Duration
    option: CsvOption

    def __init__(self: Self, path: Path, sampling_config: SamplingConfig | Freq[int] | Freq[float] | Duration, option: CsvOption) -> None:
        super().__init__()
        self.path = path
        self.config = sampling_config
        self.option = option

    def _modulation_ptr(self: Self) -> ModulationPtr:
        delim = self.option.delimiter.encode("utf-8")
        path = _to_null_terminated_utf8(str(self.path))
        return _validate_ptr(ModulationAudioFile().modulation_audio_file_csv(path, SamplingConfig(self.config)._inner, delim[0]))
