import ctypes
from collections.abc import Iterable
from typing import Self

import numpy as np

from pyautd3.derive import datagram, modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.modulation.resample import Resampler
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.utils import Duration


@datagram
@datagram_with_segment
@modulation
class Custom(Modulation):
    _buf: np.ndarray
    _config: SamplingConfig | tuple[Freq[float], SamplingConfig, Resampler]

    def __init__(self: Self, buf: Iterable[int], config: SamplingConfig | Freq[int] | Freq[float] | Duration) -> None:
        super().__init__()
        self._buf = np.fromiter(buf, dtype=np.uint8)
        self._config = config

    @staticmethod
    def new_with_resample(
        buf: Iterable[int],
        source: Freq[float],
        target: SamplingConfig | Freq[int] | Freq[float] | Duration,
        resampler: Resampler,
    ) -> "Custom":
        instance = Custom(buf, SamplingConfig(target))
        instance._config = (source, SamplingConfig(target), resampler)
        return instance

    def _modulation_ptr(self: Self) -> ModulationPtr:
        match self._config:
            case (Freq(), SamplingConfig(), Resampler()):
                (source, target, resampler) = self._config
                return Base().modulation_custom_with_resample(
                    self._loop_behavior,
                    self._buf.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
                    len(self._buf),
                    source.hz,
                    target._inner,
                    resampler._dyn_resampler(),
                )
            case _:
                return Base().modulation_custom(
                    self._config._inner,
                    self._loop_behavior,
                    self._buf.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
                    len(self._buf),
                )
