import ctypes
from collections.abc import Iterable
from datetime import timedelta

import numpy as np

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.gain.base import GainBase
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_segment_transition import DatagramST, IntoDatagramWithSegmentTransition
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.defined.freq import Freq, Hz
from pyautd3.driver.firmware.fpga import LoopBehavior
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
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
from pyautd3.native_methods.utils import _validate_f32, _validate_ptr, _validate_u64

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

    _freq: Freq[float] | None
    _freq_nearest: Freq[float] | None
    _period: timedelta | None
    _period_nearest: timedelta | None
    _sampling_config: SamplingConfig | None
    _loop_behavior: _LoopBehavior

    def __new__(cls: type["GainSTM"]) -> "GainSTM":
        raise NotImplementedError

    @classmethod
    def __private_new__(
        cls: type["GainSTM"],
        freq: Freq[float] | None,
        freq_nearest: Freq[float] | None,
        period: timedelta | None,
        period_nearest: timedelta | None,
        sampling_config: SamplingConfig | None,
        iterable: Iterable[GainBase],
    ) -> "GainSTM":
        ins = super().__new__(cls)

        ins._gains = np.array(list(iterable))
        ins._mode = GainSTMMode.PhaseIntensityFull

        ins._freq = freq
        ins._freq_nearest = freq_nearest
        ins._period = period
        ins._period_nearest = period_nearest
        ins._sampling_config = sampling_config

        ins._loop_behavior = LoopBehavior.Infinite

        return ins

    def _raw_ptr(self: "GainSTM", geometry: Geometry) -> GainSTMPtr:
        gains: np.ndarray = np.ndarray(len(self._gains), dtype=GainPtr)
        for i, g in enumerate(self._gains):
            gains[i]["_0"] = g._gain_ptr(geometry)._0
        return self._ptr(gains)

    def _ptr(self: "GainSTM", gains: np.ndarray) -> GainSTMPtr:
        ptr: GainSTMPtr
        if self._freq is not None:
            ptr = _validate_ptr(
                Base().stm_gain_from_freq(
                    self._freq.hz,
                    gains.ctypes.data_as(ctypes.POINTER(GainPtr)),  # type: ignore[arg-type]
                    len(gains),
                ),
            )
        elif self._freq_nearest is not None:
            ptr = _validate_ptr(
                Base().stm_gain_from_freq_nearest(
                    self._freq_nearest.hz,
                    gains.ctypes.data_as(ctypes.POINTER(GainPtr)),  # type: ignore[arg-type]
                    len(gains),
                ),
            )
        elif self._period is not None:
            ptr = _validate_ptr(
                Base().stm_gain_from_period(
                    int(self._period.total_seconds() * 1000 * 1000 * 1000),
                    gains.ctypes.data_as(ctypes.POINTER(GainPtr)),  # type: ignore[arg-type]
                    len(gains),
                ),
            )
        elif self._period_nearest is not None:
            ptr = _validate_ptr(
                Base().stm_gain_from_period_nearest(
                    int(self._period_nearest.total_seconds() * 1000 * 1000 * 1000),
                    gains.ctypes.data_as(ctypes.POINTER(GainPtr)),  # type: ignore[arg-type]
                    len(gains),
                ),
            )
        else:
            ptr = Base().stm_gain_from_sampling_config(
                self._sampling_config._inner,  # type: ignore[union-attr]
                gains.ctypes.data_as(ctypes.POINTER(GainPtr)),  # type: ignore[arg-type]
                len(gains),
            )
        ptr = Base().stm_gain_with_mode(ptr, self._mode)
        ptr = Base().stm_gain_with_loop_behavior(ptr, self._loop_behavior)
        return ptr

    def _datagram_ptr(self: "GainSTM", geometry: Geometry) -> DatagramPtr:
        return Base().stm_gain_into_datagram(self._raw_ptr(geometry))

    def _into_segment_transition(self: "GainSTM", ptr: GainSTMPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        if transition_mode is None:
            return Base().stm_gain_into_datagram_with_segment(ptr, segment)
        return Base().stm_gain_into_datagram_with_segment_transition(ptr, segment, transition_mode)

    @staticmethod
    def from_freq(freq: Freq[float], iterable: Iterable[GainBase]) -> "GainSTM":
        return GainSTM.__private_new__(freq, None, None, None, None, iterable)

    @staticmethod
    def from_freq_nearest(freq: Freq[float], iterable: Iterable[GainBase]) -> "GainSTM":
        return GainSTM.__private_new__(None, freq, None, None, None, iterable)

    @staticmethod
    def from_period(period: timedelta, iterable: Iterable[GainBase]) -> "GainSTM":
        return GainSTM.__private_new__(None, None, period, None, None, iterable)

    @staticmethod
    def from_period_nearest(period: timedelta, iterable: Iterable[GainBase]) -> "GainSTM":
        return GainSTM.__private_new__(None, None, None, period, None, iterable)

    @staticmethod
    def from_sampling_config(config: SamplingConfig | Freq[int] | timedelta, iterable: Iterable[GainBase]) -> "GainSTM":
        return GainSTM.__private_new__(None, None, None, None, SamplingConfig(config), iterable)

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
        gains: np.ndarray = np.ndarray(len(self._gains), dtype=GainPtr)
        for i in range(len(self._gains)):
            gains[i]["_0"] = Base().gain_null()._0
        return _validate_f32(Base().stm_gain_freq(self._ptr(gains))) * Hz

    @property
    def period(self: "GainSTM") -> timedelta:
        gains: np.ndarray = np.ndarray(len(self._gains), dtype=GainPtr)
        for i in range(len(self._gains)):
            gains[i]["_0"] = Base().gain_null()._0
        return timedelta(microseconds=_validate_u64(Base().stm_gain_period(self._ptr(gains))) / 1000)
