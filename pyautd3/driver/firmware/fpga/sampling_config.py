from typing import Self

import numpy as np

from pyautd3.driver.common import Freq
from pyautd3.driver.common.freq import Hz
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import SamplingConfigWrap
from pyautd3.native_methods.utils import _validate_duration, _validate_f32, _validate_sampling_config, _validate_u16
from pyautd3.utils import Duration


class SamplingConfig:
    _inner: SamplingConfigWrap

    def __init__(self: Self, value: "SamplingConfigWrap | SamplingConfig | int | Freq[int] | Freq[float] | Duration") -> None:
        match value:
            case int() | np.integer():
                value = int(value)
                if value > 0xFFFF:  # noqa: PLR2004
                    raise ValueError
                self._inner = _validate_sampling_config(Base().sampling_config_from_divide(value))
            case SamplingConfigWrap():
                self._inner = value
            case SamplingConfig():
                self._inner = value._inner
            case Freq():
                match value.hz():
                    case float() as v:
                        self._inner = Base().sampling_config_from_freq(v)
                    case _:
                        raise TypeError
            case Duration():
                self._inner = Base().sampling_config_from_period(value._inner)
            case _:
                raise TypeError

    def into_nearest(self: Self) -> "SamplingConfig":
        return SamplingConfig(Base().sampling_config_into_nearest(self._inner))

    @property
    def divide(self: Self) -> int:
        return _validate_u16(Base().sampling_config_divide(self._inner))

    def freq(self: Self) -> Freq[float]:
        return _validate_f32(Base().sampling_config_freq(self._inner)) * Hz

    def period(self: Self) -> Duration:
        return Duration.__private_new__(_validate_duration(Base().sampling_config_period(self._inner)))

    def __eq__(self: Self, value: object) -> bool:
        return isinstance(value, SamplingConfig) and bool(Base().sampling_config_eq(self._inner, value._inner))

    def __hash__(self: Self) -> int:
        return self._inner.__hash__()  # pragma: no cover

    FREQ_40K: "SamplingConfig" = None  # type: ignore[assignment]
    FREQ_4K: "SamplingConfig" = None  # type: ignore[assignment]


SamplingConfig.FREQ_40K = SamplingConfig(40000.0 * Hz)
SamplingConfig.FREQ_4K = SamplingConfig(4000.0 * Hz)
