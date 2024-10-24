import ctypes
from collections.abc import Iterable
from datetime import timedelta
from typing import Self

import numpy as np

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.gain.base import GainBase
from pyautd3.driver.datagram.stm.stm_sampling_config import STMSamplingConfig
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_segment import DatagramS, IntoDatagramWithSegment
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga import LoopBehavior
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
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
    IntoDatagramWithSegment,
    IntoDatagramWithTimeout["GainSTM"],
    IntoDatagramWithParallelThreshold["GainSTM"],
    DatagramS[GainSTMPtr],
    Datagram,
):
    _gains: np.ndarray
    _mode: GainSTMMode

    _stm_sampling_config: STMSamplingConfig
    _loop_behavior: _LoopBehavior

    def __private_init__(
        self: Self,
        sampling_config: STMSamplingConfig,
        gains: list[GainBase],
    ) -> None:
        self._gains = np.array(gains)
        self._mode = GainSTMMode.PhaseIntensityFull

        self._stm_sampling_config = sampling_config
        self._loop_behavior = LoopBehavior.Infinite

    def __init__(
        self: Self,
        config: "SamplingConfig | Freq[float] | timedelta",
        iterable: Iterable[GainBase],
    ) -> None:
        gains = list(iterable)
        self.__private_init__(STMSamplingConfig(config, len(gains)), gains)

    @classmethod
    def nearest(
        cls: type["GainSTM"],
        config: "Freq[float] | timedelta",
        iterable: Iterable[GainBase],
    ) -> "GainSTM":
        ins = cls.__new__(cls)
        gains = list(iterable)
        ins.__private_init__(STMSamplingConfig._nearest(config, len(gains)), gains)
        return ins

    def _raw_ptr(self: Self, geometry: Geometry) -> GainSTMPtr:
        gains: np.ndarray = np.ndarray(len(self._gains), dtype=GainPtr)
        for i, g in enumerate(self._gains):
            gains[i]["_0"] = g._gain_ptr(geometry)._0
        return self._ptr(gains)

    def _ptr(self: Self, gains: np.ndarray) -> GainSTMPtr:
        return _validate_ptr(
            Base().stm_gain(
                self._stm_sampling_config._inner,
                gains.ctypes.data_as(ctypes.POINTER(GainPtr)),  # type: ignore[arg-type]
                len(gains),
                self._mode,
                self._loop_behavior,
            ),
        )

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return Base().stm_gain_into_datagram(self._raw_ptr(geometry))

    def _into_segment(self: Self, ptr: GainSTMPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        return Base().stm_gain_into_datagram_with_segment(
            ptr,
            segment,
            transition_mode if transition_mode is not None else TransitionMode.NONE,
        )

    def with_mode(self: Self, mode: GainSTMMode) -> Self:
        self._mode = mode
        return self

    @property
    def mode(self: Self) -> GainSTMMode:
        return self._mode

    def with_loop_behavior(self: Self, value: _LoopBehavior) -> Self:
        self._loop_behavior = value
        return self

    @property
    def freq(self: Self) -> Freq[float]:
        return self._stm_sampling_config.freq()

    @property
    def period(self: Self) -> timedelta:
        return self._stm_sampling_config.period()

    @property
    def sampling_config(self: Self) -> SamplingConfig:
        return self._stm_sampling_config.sampling_config()

    def _sampling_config_intensity(self: Self) -> SamplingConfig:
        return self.sampling_config

    def _sampling_config_phase(self: Self) -> SamplingConfig:
        return self.sampling_config
