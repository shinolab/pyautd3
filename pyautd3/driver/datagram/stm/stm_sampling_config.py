from typing import Self

from pyautd3.driver.defined import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.utils import _validate_sampling_config
from pyautd3.utils import Duration


class FreqNearest:
    freq: Freq[float]

    def __init__(self: Self, freq: Freq[float]) -> None:
        self.freq = freq


class PeriodNearest:
    period: Duration

    def __init__(self: Self, period: Duration) -> None:
        self.period = period


def _sampling_config(config: SamplingConfig | Freq[float] | Duration | FreqNearest | PeriodNearest, n: int) -> SamplingConfig:
    match config:
        case SamplingConfig() as value:
            return value
        case Freq() as value:
            return SamplingConfig(_validate_sampling_config(Base().stm_config_from_freq(value.hz(), n)))
        case Duration() as value:
            return SamplingConfig(_validate_sampling_config(Base().stm_config_from_period(value._inner, n)))
        case FreqNearest() as value:
            return SamplingConfig(Base().stm_config_from_freq_nearest(value.freq.hz(), n))
        case PeriodNearest() as value:  # pragma: no cover
            return SamplingConfig(Base().stm_config_from_period_nearest(value.period._inner, n))
