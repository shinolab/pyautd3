from datetime import timedelta

from pyautd3.driver.defined import Freq
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.utils import _validate_nonzero_u16
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.structs import SamplingConfig as _SamplingConfig
from pyautd3.native_methods.utils import _validate_sampling_config


class SamplingConfig:
    _inner: _SamplingConfig

    def __init__(self: "SamplingConfig", inner: "_SamplingConfig | SamplingConfig | int | Freq[int] | Freq[float] | timedelta") -> None:
        if isinstance(inner, int):
            self._inner = Base().sampling_config_from_division(_validate_nonzero_u16(inner))
        elif isinstance(inner, _SamplingConfig):
            self._inner = inner
        elif isinstance(inner, SamplingConfig):
            self._inner = inner._inner
        elif isinstance(inner, Freq):
            if isinstance(inner.hz, int):
                self._inner = _validate_sampling_config(Base().sampling_config_from_freq(inner.hz))
            elif isinstance(inner.hz, float):
                self._inner = _validate_sampling_config(Base().sampling_config_from_freq_f(inner.hz))
            else:
                raise TypeError
        elif isinstance(inner, timedelta):
            self._inner = _validate_sampling_config(
                Base().sampling_config_from_period(int(inner.total_seconds() * 1000 * 1000 * 1000)),
            )
        else:
            raise TypeError

    @staticmethod
    def _nearest(freq: Freq[float] | timedelta) -> "SamplingConfig":
        if isinstance(freq, Freq):
            return SamplingConfig(Base().sampling_config_from_freq_nearest(freq.hz))
        if isinstance(freq, timedelta):
            return SamplingConfig(
                Base().sampling_config_from_period_nearest(int(freq.total_seconds() * 1000 * 1000 * 1000)),
            )
        raise TypeError

    @property
    def division(self: "SamplingConfig") -> int:
        return int(Base().sampling_config_division(self._inner))

    @property
    def freq(self: "SamplingConfig") -> Freq[float]:
        return float(Base().sampling_config_freq(self._inner)) * Hz

    @property
    def period(self: "SamplingConfig") -> timedelta:
        return timedelta(microseconds=int(Base().sampling_config_period(self._inner)) / 1000)

    def __eq__(self: "SamplingConfig", value: object) -> bool:
        return isinstance(value, SamplingConfig) and self._inner.div == self._inner.div
