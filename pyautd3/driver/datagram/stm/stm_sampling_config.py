from datetime import timedelta

from pyautd3.driver.defined import Freq
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import STMConfigWrap
from pyautd3.native_methods.utils import _validate_f32, _validate_sampling_config, _validate_u64


class STMSamplingConfig:
    _inner: STMConfigWrap

    def __init__(self: "STMSamplingConfig", inner: "STMConfigWrap | SamplingConfig | Freq[float] | timedelta") -> None:
        if isinstance(inner, STMConfigWrap):
            self._inner = inner
        elif isinstance(inner, SamplingConfig):
            self._inner = Base().stm_config_from_sampling_config(inner._inner)
        elif isinstance(inner, Freq):
            self._inner = Base().stm_config_from_freq(inner.hz)
        elif isinstance(inner, timedelta):
            self._inner = Base().stm_config_from_period(
                int(inner.total_seconds() * 1000 * 1000 * 1000),
            )

    @staticmethod
    def _nearest(inner: "Freq[float] | timedelta") -> "STMSamplingConfig":
        if isinstance(inner, Freq):
            return STMSamplingConfig(Base().stm_config_from_freq_nearest(inner.hz))
        if isinstance(inner, timedelta):
            return STMSamplingConfig(
                Base().stm_config_from_period_nearest(int(inner.total_seconds() * 1000 * 1000 * 1000)),
            )
        raise TypeError

    @staticmethod
    def FreqNearest(freq: Freq[float]) -> "STMSamplingConfig":  # noqa: N802
        return STMSamplingConfig(Base().stm_config_from_freq_nearest(freq.hz))

    @staticmethod
    def PeriodNearest(period: timedelta) -> "STMSamplingConfig":  # noqa: N802
        return STMSamplingConfig(Base().stm_config_from_period_nearest(int(period.total_seconds() * 1000 * 1000 * 1000)))

    def freq(self: "STMSamplingConfig", n: int) -> Freq[float]:
        return _validate_f32(Base().stm_freq(self._inner, n)) * Hz

    def period(self: "STMSamplingConfig", n: int) -> timedelta:
        return timedelta(microseconds=_validate_u64(Base().stm_period(self._inner, n)) / 1000)

    def sampling_config(self: "STMSamplingConfig", n: int) -> SamplingConfig:
        return SamplingConfig(_validate_sampling_config(Base().stm_sampling_sampling_config(self._inner, n)))
