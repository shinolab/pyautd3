from datetime import timedelta
from typing import Self

from pyautd3.driver.defined import Freq
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.native_methods.autd3_driver import SamplingConfig as _SamplingConfig
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.utils import _validate_sampling_config


class STMSamplingConfig:
    _inner: _SamplingConfig
    _n: int

    def __init__(self: Self, value: "_SamplingConfig | SamplingConfig | Freq[float] | timedelta", n: int) -> None:
        match value:
            case _SamplingConfig():
                self._inner = value
            case SamplingConfig():
                self._inner = value._inner
            case Freq():
                match value.hz:
                    case float():
                        self._inner = _validate_sampling_config(Base().stm_config_from_freq(value.hz, n))
                    case _:
                        raise TypeError
            case timedelta():
                self._inner = _validate_sampling_config(
                    Base().stm_config_from_period(int(value.total_seconds() * 1000 * 1000 * 1000), n),
                )
            case _:
                raise TypeError
        self._n = n

    @staticmethod
    def _nearest(value: "Freq[float] | timedelta", n: int) -> "STMSamplingConfig":
        match value:
            case Freq():
                match value.hz:
                    case float():
                        return STMSamplingConfig(_validate_sampling_config(Base().stm_config_from_freq_nearest(value.hz, n)), n)
                    case _:
                        raise TypeError
            case timedelta():
                return STMSamplingConfig(
                    _validate_sampling_config(
                        Base().stm_config_from_period_nearest(int(value.total_seconds() * 1000 * 1000 * 1000), n),
                    ),
                    n,
                )
            case _:
                raise TypeError

    def freq(self: Self) -> Freq[float]:
        return float(Base().stm_freq(self._inner, self._n)) * Hz

    def period(self: Self) -> timedelta:
        return timedelta(microseconds=int(Base().stm_period(self._inner, self._n)) / 1000)

    def sampling_config(self: Self) -> SamplingConfig:
        return SamplingConfig(self._inner)
