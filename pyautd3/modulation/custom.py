import ctypes
from collections.abc import Iterable
from typing import Self

import numpy as np

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.utils import Duration


class Custom(Modulation):
    buffer: np.ndarray
    config: SamplingConfig | Freq[int] | Freq[float] | Duration

    def __init__(self: Self, buffer: Iterable[int], sampling_config: SamplingConfig | Freq[int] | Freq[float] | Duration) -> None:
        super().__init__()
        self.buffer = np.fromiter(buffer, dtype=np.uint8)
        self.config = sampling_config

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return Base().modulation_custom(
            self.buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
            len(self.buffer),
            SamplingConfig(self.config)._inner,
        )
