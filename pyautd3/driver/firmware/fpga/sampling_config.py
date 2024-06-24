from datetime import timedelta

from pyautd3.driver.defined import Freq as _Freq
from pyautd3.driver.defined.freq import Hz
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import SamplingConfigWrap
from pyautd3.native_methods.utils import _validate_f32, _validate_u32, _validate_u64


class SamplingConfig:
    _inner: SamplingConfigWrap

    def __init__(self: "SamplingConfig", inner: "SamplingConfigWrap | SamplingConfig | _Freq[int] | timedelta") -> None:
        if isinstance(inner, SamplingConfigWrap):
            self._inner = inner
        elif isinstance(inner, SamplingConfig):
            self._inner = inner._inner
        elif isinstance(inner, _Freq):
            self._inner = SamplingConfig.Freq(inner)._inner
        elif isinstance(inner, timedelta):
            self._inner = SamplingConfig.Period(inner)._inner
        else:
            raise TypeError

    @staticmethod
    def Freq(freq: _Freq[int]) -> "SamplingConfig":  # noqa: N802
        return SamplingConfig(Base().sampling_config_from_freq(freq.hz))

    @staticmethod
    def FreqNearest(freq: _Freq[float]) -> "SamplingConfig":  # noqa: N802
        return SamplingConfig(Base().sampling_config_from_freq_nearest(freq.hz))

    @staticmethod
    def Period(period: timedelta) -> "SamplingConfig":  # noqa: N802
        return SamplingConfig(Base().sampling_config_from_period(int(period.total_seconds() * 1000 * 1000 * 1000)))

    @staticmethod
    def PeriodNearest(period: timedelta) -> "SamplingConfig":  # noqa: N802
        return SamplingConfig(Base().sampling_config_from_period_nearest(int(period.total_seconds() * 1000 * 1000 * 1000)))

    @staticmethod
    def Division(div: int) -> "SamplingConfig":  # noqa: N802
        return SamplingConfig(Base().sampling_config_from_division(div))

    @staticmethod
    def DivisionRaw(div: int) -> "SamplingConfig":  # noqa: N802
        return SamplingConfig(Base().sampling_config_from_division_raw(div))

    @property
    def division(self: "SamplingConfig") -> int:
        return _validate_u32(Base().sampling_config_division(self._inner))

    @property
    def freq(self: "SamplingConfig") -> _Freq[float]:
        return _validate_f32(Base().sampling_config_freq(self._inner)) * Hz

    @property
    def period(self: "SamplingConfig") -> timedelta:
        return timedelta(microseconds=_validate_u64(Base().sampling_config_period(self._inner)) / 1000)

    def __eq__(self: "SamplingConfig", value: object) -> bool:
        return isinstance(value, SamplingConfig) and self.division == value.division
