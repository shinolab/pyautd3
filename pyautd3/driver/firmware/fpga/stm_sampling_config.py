from datetime import timedelta

from pyautd3.driver.defined import Freq as _Freq
from pyautd3.driver.defined.freq import Hz
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import STMSamplingConfigWrap
from pyautd3.native_methods.utils import _validate_f32, _validate_sampling_config, _validate_u64

from .sampling_config import SamplingConfig as _SamplingConfig


class STMSamplingConfig:
    _inner: STMSamplingConfigWrap

    def __init__(self: "STMSamplingConfig", inner: STMSamplingConfigWrap) -> None:
        self._inner = inner

    @staticmethod
    def Freq(freq: _Freq[float]) -> "STMSamplingConfig":  # noqa: N802
        return STMSamplingConfig(Base().stm_sampling_config_from_freq(freq.hz))

    @staticmethod
    def FreqNearest(freq: _Freq[float]) -> "STMSamplingConfig":  # noqa: N802
        return STMSamplingConfig(Base().stm_sampling_config_from_freq_nearest(freq.hz))

    @staticmethod
    def Period(period: timedelta) -> "STMSamplingConfig":  # noqa: N802
        return STMSamplingConfig(Base().stm_sampling_config_from_period(int(period.total_seconds() * 1000 * 1000 * 1000)))

    @staticmethod
    def PeriodNearest(period: timedelta) -> "STMSamplingConfig":  # noqa: N802
        return STMSamplingConfig(Base().stm_sampling_config_from_period_nearest(int(period.total_seconds() * 1000 * 1000 * 1000)))

    @staticmethod
    def SamplingConfig(config: _SamplingConfig) -> "STMSamplingConfig":  # noqa: N802
        return STMSamplingConfig(Base().stm_sampling_config_from_sampling_config(config._inner))

    def freq(self: "STMSamplingConfig", n: int) -> _Freq[float]:
        return _validate_f32(Base().stm_freq(self._inner, n)) * Hz

    def period(self: "STMSamplingConfig", n: int) -> timedelta:
        return timedelta(microseconds=_validate_u64(Base().stm_period(self._inner, n)) / 1000)

    def sampling_config(self: "STMSamplingConfig", n: int) -> _SamplingConfig:
        return _SamplingConfig(_validate_sampling_config(Base().stm_sampling_sampling_config(self._inner, n)))
