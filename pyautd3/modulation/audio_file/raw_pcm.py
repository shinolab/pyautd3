from datetime import timedelta
from pathlib import Path

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.datagram.modulation.transform import IntoModulationTransform
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.autd3capi_modulation_audio_file import (
    NativeMethods as ModulationAudioFile,
)
from pyautd3.native_methods.utils import _validate_ptr


class RawPCM(
    IntoModulationCache["RawPCM"],
    IntoModulationTransform["RawPCM"],
    IntoModulationRadiationPressure["RawPCM"],
    ModulationBase["RawPCM"],
):
    _path: Path
    _config: SamplingConfig
    _sample_rate: Freq[int]

    def __init__(self: "RawPCM", path: Path, config: SamplingConfig | Freq[int] | Freq[float] | timedelta) -> None:
        super().__init__()
        self._path = path
        self._config = SamplingConfig(config)

    def _modulation_ptr(self: "RawPCM") -> ModulationPtr:
        return _validate_ptr(
            ModulationAudioFile().modulation_audio_file_raw_pcm(
                str(self._path).encode("utf-8"),
                self._config._inner,
                self._loop_behavior,
            ),
        )
