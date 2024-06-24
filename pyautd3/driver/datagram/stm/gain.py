import ctypes
from collections.abc import Iterable
from datetime import timedelta

import numpy as np

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.gain.base import GainBase
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_segment_transition import DatagramST, IntoDatagramWithSegmentTransition
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga import LoopBehavior
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.firmware.fpga.stm_sampling_config import STMSamplingConfig
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import (
    DatagramPtr,
    GainPtr,
    GainSTMMode,
    GainSTMPtr,
    Segment,
    TransitionModeWrap,
)
from pyautd3.native_methods.autd3capi_driver import LoopBehavior as _LoopBehavior
from pyautd3.native_methods.utils import _validate_ptr

__all__ = []  # type: ignore[var-annotated]


class GainSTM(
    IntoDatagramWithSegmentTransition,
    IntoDatagramWithTimeout["GainSTM"],
    IntoDatagramWithParallelThreshold["GainSTM"],
    DatagramST[GainSTMPtr],
    Datagram,
):
    _gains: np.ndarray
    _mode: GainSTMMode

    _stm_sampling_config: STMSamplingConfig
    _loop_behavior: _LoopBehavior

    def __new__(cls: type["GainSTM"]) -> "GainSTM":
        raise NotImplementedError

    @classmethod
    def __private_new__(
        cls: type["GainSTM"],
        sampling_config: STMSamplingConfig,
        iterable: Iterable[GainBase],
    ) -> "GainSTM":
        ins = super().__new__(cls)

        ins._gains = np.array(list(iterable))
        ins._mode = GainSTMMode.PhaseIntensityFull

        ins._stm_sampling_config = sampling_config

        ins._loop_behavior = LoopBehavior.Infinite

        return ins

    def _raw_ptr(self: "GainSTM", geometry: Geometry) -> GainSTMPtr:
        gains: np.ndarray = np.ndarray(len(self._gains), dtype=GainPtr)
        for i, g in enumerate(self._gains):
            gains[i]["_0"] = g._gain_ptr(geometry)._0
        return self._ptr(gains)

    def _ptr(self: "GainSTM", gains: np.ndarray) -> GainSTMPtr:
        ptr: GainSTMPtr = _validate_ptr(
            Base().stm_gain(
                self._stm_sampling_config._inner,
                gains.ctypes.data_as(ctypes.POINTER(GainPtr)),  # type: ignore[arg-type]
                len(gains),
            ),
        )
        ptr = Base().stm_gain_with_mode(ptr, self._mode)
        return Base().stm_gain_with_loop_behavior(ptr, self._loop_behavior)

    def _datagram_ptr(self: "GainSTM", geometry: Geometry) -> DatagramPtr:
        return Base().stm_gain_into_datagram(self._raw_ptr(geometry))

    def _into_segment_transition(self: "GainSTM", ptr: GainSTMPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        if transition_mode is None:
            return Base().stm_gain_into_datagram_with_segment(ptr, segment)
        return Base().stm_gain_into_datagram_with_segment_transition(ptr, segment, transition_mode)

    @staticmethod
    def from_freq(freq: Freq[float], iterable: Iterable[GainBase]) -> "GainSTM":
        return GainSTM.__private_new__(STMSamplingConfig.Freq(freq), iterable)

    @staticmethod
    def from_freq_nearest(freq: Freq[float], iterable: Iterable[GainBase]) -> "GainSTM":
        return GainSTM.__private_new__(STMSamplingConfig.FreqNearest(freq), iterable)

    @staticmethod
    def from_period(period: timedelta, iterable: Iterable[GainBase]) -> "GainSTM":
        return GainSTM.__private_new__(STMSamplingConfig.Period(period), iterable)

    @staticmethod
    def from_period_nearest(period: timedelta, iterable: Iterable[GainBase]) -> "GainSTM":
        return GainSTM.__private_new__(STMSamplingConfig.PeriodNearest(period), iterable)

    @staticmethod
    def from_sampling_config(config: SamplingConfig | Freq[int] | timedelta, iterable: Iterable[GainBase]) -> "GainSTM":
        return GainSTM.__private_new__(STMSamplingConfig.SamplingConfig(SamplingConfig(config)), iterable)

    def with_mode(self: "GainSTM", mode: GainSTMMode) -> "GainSTM":
        self._mode = mode
        return self

    @property
    def mode(self: "GainSTM") -> GainSTMMode:
        return self._mode

    def with_loop_behavior(self: "GainSTM", value: _LoopBehavior) -> "GainSTM":
        self._loop_behavior = value
        return self

    @property
    def freq(self: "GainSTM") -> Freq[float]:
        return self._stm_sampling_config.freq(len(self._gains))

    @property
    def period(self: "GainSTM") -> timedelta:
        return self._stm_sampling_config.period(len(self._gains))

    @property
    def sampling_config(self: "GainSTM") -> SamplingConfig:
        return self._stm_sampling_config.sampling_config(len(self._gains))
