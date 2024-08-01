from datetime import timedelta

from pyautd3.driver.defined import Freq
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.structs import SamplingConfig as _SamplingConfig
from pyautd3.native_methods.utils import _validate_sampling_config


class STMSamplingConfig:
    _inner: _SamplingConfig
    _n: int

    def __init__(self: "STMSamplingConfig", inner: "_SamplingConfig | SamplingConfig | Freq[float] | timedelta", n: int) -> None:
        if isinstance(inner, _SamplingConfig):
            self._inner = inner
        elif isinstance(inner, SamplingConfig):
            self._inner = inner._inner
        elif isinstance(inner, Freq):
            self._inner = _validate_sampling_config(Base().stm_config_from_freq(inner.hz, n))
        elif isinstance(inner, timedelta):
            self._inner = _validate_sampling_config(
                Base().stm_config_from_period(int(inner.total_seconds() * 1000 * 1000 * 1000), n),
            )
        else:
            raise TypeError
        self._n = n

    @staticmethod
    def _nearest(inner: "Freq[float] | timedelta", n: int) -> "STMSamplingConfig":
        if isinstance(inner, Freq):
            return STMSamplingConfig(_validate_sampling_config(Base().stm_config_from_freq_nearest(inner.hz, n)), n)
        if isinstance(inner, timedelta):
            return STMSamplingConfig(
                _validate_sampling_config(
                    Base().stm_config_from_period_nearest(int(inner.total_seconds() * 1000 * 1000 * 1000), n),
                ),
                n,
            )
        raise TypeError

    def freq(self: "STMSamplingConfig") -> Freq[float]:
        return float(Base().stm_freq(self._inner, self._n)) * Hz

    def period(self: "STMSamplingConfig") -> timedelta:
        return timedelta(microseconds=int(Base().stm_period(self._inner, self._n)) / 1000)

    def sampling_config(self: "STMSamplingConfig") -> SamplingConfig:
        return SamplingConfig(self._inner)
