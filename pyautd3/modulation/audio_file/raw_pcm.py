from pathlib import Path

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.geometry.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import (
    NativeMethods as ModulationAudioFile,
)
from pyautd3.native_methods.utils import _validate_ptr


class RawPCM(Modulation["RawPCM"]):
    _path: Path
    _sample_rate: Freq[int]

    def __init__(self: "RawPCM", path: Path, sample_rate: Freq[int]) -> None:
        super().__init__(SamplingConfig.Division(5120))
        self._path = path
        self._sample_rate = sample_rate

    def _modulation_ptr(self: "RawPCM", _: Geometry) -> ModulationPtr:
        return _validate_ptr(
            ModulationAudioFile().modulation_raw_pcm(
                str(self._path).encode("utf-8"),
                self._sample_rate.hz,
                self._config,
                self._loop_behavior,
            ),
        )
