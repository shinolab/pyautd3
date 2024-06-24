import ctypes
from datetime import timedelta

import numpy as np

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr


class Custom(Modulation["Custom"]):
    _buf: np.ndarray

    def __init__(self: "Custom", buf: np.ndarray, config: SamplingConfig | Freq[int] | timedelta) -> None:
        super().__init__(config)
        self._buf = buf

    def _modulation_ptr(self: "Custom") -> ModulationPtr:
        return Base().modulation_raw(
            self._config._inner,
            self._loop_behavior,
            self._buf.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
            len(self._buf),
        )
