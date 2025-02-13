from typing import Self

from pyautd3.driver.defined import Freq
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.utils import _validate_nonzero_u16
from pyautd3.native_methods.autd3 import SamplingConfig as _SamplingConfig
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.utils import _validate_sampling_config
from pyautd3.utils import Duration


class SamplingConfig:
    _inner: _SamplingConfig

    def __init__(self: Self, value: "_SamplingConfig | SamplingConfig | int | Freq[int] | Freq[float] | Duration") -> None:
        match value:
            case int():
                self._inner = _validate_sampling_config(Base().sampling_config_from_division(_validate_nonzero_u16(value)))
            case _SamplingConfig():
                self._inner = value
            case SamplingConfig():
                self._inner = value._inner
            case Freq():
                match value.hz():
                    case int() as v:
                        self._inner = _validate_sampling_config(Base().sampling_config_from_freq(v))
                    case float() as v:
                        self._inner = _validate_sampling_config(Base().sampling_config_from_freq_f(v))
                    case _:
                        raise TypeError
            case Duration():
                self._inner = _validate_sampling_config(Base().sampling_config_from_period(value._inner))
            case _:
                raise TypeError

    @staticmethod
    def nearest(value: Freq[float] | Duration) -> "SamplingConfig":
        match value:
            case Freq():
                match value.hz():
                    case float() as v:
                        return SamplingConfig(Base().sampling_config_from_freq_nearest(v))
                    case _:
                        raise TypeError
            case Duration():
                return SamplingConfig(Base().sampling_config_from_period_nearest(value._inner))
            case _:
                raise TypeError

    @property
    def division(self: Self) -> int:
        return int(Base().sampling_config_division(self._inner))

    def freq(self: Self) -> Freq[float]:
        return float(Base().sampling_config_freq(self._inner)) * Hz

    def period(self: Self) -> Duration:
        return Duration.__private_new__(Base().sampling_config_period(self._inner))

    def __eq__(self: Self, value: object) -> bool:
        return isinstance(value, SamplingConfig) and self._inner.division == self._inner.division

    FREQ_40K: "SamplingConfig" = None  # type: ignore[assignment]
    FREQ_4K: "SamplingConfig" = None  # type: ignore[assignment]


SamplingConfig.FREQ_40K = SamplingConfig(1)
SamplingConfig.FREQ_4K = SamplingConfig(10)
