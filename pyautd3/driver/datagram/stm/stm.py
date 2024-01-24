from abc import ABCMeta
from datetime import timedelta

from pyautd3.driver.common.sampling_config import SamplingConfiguration
from pyautd3.driver.datagram import Datagram
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import STMPropsPtr
from pyautd3.native_methods.utils import _validate_sampling_config


class _STM(Datagram, metaclass=ABCMeta):
    _freq: float | None
    _period: timedelta | None
    _sampling_config: SamplingConfiguration | None
    _start_idx: int
    _finish_idx: int

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
        self._start_idx = -1
        self._finish_idx = -1

    @property
    def start_idx(self: "_STM") -> int | None:
        """Start index of STM."""
        idx = int(Base().stm_props_start_idx(self._props()))
        if idx < 0:
            return None
        return idx

    @property
    def finish_idx(self: "_STM") -> int | None:
        """Finish index of STM."""
        idx = int(Base().stm_props_finish_idx(self._props()))
        if idx < 0:
            return None
        return idx

    def _props(self: "_STM") -> STMPropsPtr:
        ptr: STMPropsPtr
        if self._freq is not None:
            ptr = Base().stm_props_from_freq(self._freq)
        if self._period is not None:
            ptr = Base().stm_props_from_period(int(self._period.total_seconds() * 1000 * 1000 * 1000))
        if self._sampling_config is not None:
            ptr = Base().stm_props_from_sampling_config(self._sampling_config._internal)
        ptr = Base().stm_props_with_start_idx(ptr, self._start_idx)
        return Base().stm_props_with_finish_idx(ptr, self._finish_idx)

    def _frequency_from_size(self: "_STM", size: int) -> float:
        return float(Base().stm_props_frequency(self._props(), size))

    def _period_from_size(self: "_STM", size: int) -> timedelta:
        return timedelta(seconds=int(Base().stm_props_period(self._props(), size)) / 1000.0 / 1000.0 / 1000.0)

    def _sampling_config_from_size(self: "_STM", size: int) -> SamplingConfiguration:
        return SamplingConfiguration.__private_new__(_validate_sampling_config(Base().stm_props_sampling_config(self._props(), size)))
