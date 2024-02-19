from abc import ABCMeta
from datetime import timedelta

from pyautd3.driver.common import LoopBehavior, SamplingConfiguration
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import STMPropsPtr
from pyautd3.native_methods.utils import _validate_sampling_config


class _STM(metaclass=ABCMeta):
    _freq: float | None
    _period: timedelta | None
    _sampling_config: SamplingConfiguration | None
    _loop_behavior: LoopBehavior

    def __init__(
        self: "_STM",
        freq: float | None,
        period: timedelta | None,
        sampling_config: SamplingConfiguration | None,
    ) -> None:
        super().__init__()
        self._freq = freq
        self._period = period
        self._sampling_config = sampling_config
        self._loop_behavior = LoopBehavior.infinite()

    @property
    def loop_behavior(self: "_STM") -> LoopBehavior:
        """Loop behavior of STM."""
        return self._loop_behavior

    def _props(self: "_STM") -> STMPropsPtr:
        ptr: STMPropsPtr
        if self._freq is not None:
            ptr = Base().stm_props_from_freq(self._freq)
        if self._period is not None:
            ptr = Base().stm_props_from_period(int(self._period.total_seconds() * 1000 * 1000 * 1000))
        if self._sampling_config is not None:
            ptr = Base().stm_props_from_sampling_config(self._sampling_config._internal)
        return Base().stm_props_with_loop_behavior(ptr, self._loop_behavior._internal)

    def _frequency_from_size(self: "_STM", size: int) -> float:
        return float(Base().stm_props_frequency(self._props(), size))

    def _period_from_size(self: "_STM", size: int) -> timedelta:
        return timedelta(seconds=int(Base().stm_props_period(self._props(), size)) / 1000.0 / 1000.0 / 1000.0)

    def _sampling_config_from_size(self: "_STM", size: int) -> SamplingConfiguration:
        return SamplingConfiguration.__private_new__(_validate_sampling_config(Base().stm_props_sampling_config(self._props(), size)))
