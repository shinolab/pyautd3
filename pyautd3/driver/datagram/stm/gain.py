import ctypes
from collections.abc import Iterable
from datetime import timedelta

import numpy as np

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.gain.base import GainBase
from pyautd3.driver.datagram.stm.stm_sampling_config import STMSamplingConfig
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_segment_transition import DatagramST, IntoDatagramWithSegmentTransition
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.defined.freq import Freq
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

    def __private_init__(
        self: "GainSTM",
        sampling_config: STMSamplingConfig,
        gains: list[GainBase],
    ) -> None:
        self._gains = np.array(gains)
        self._mode = GainSTMMode.PhaseIntensityFull

        self._stm_sampling_config = sampling_config
        self._loop_behavior = LoopBehavior.Infinite

    def __init__(
        self: "GainSTM",
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
        return self._stm_sampling_config.freq()

    @property
    def period(self: "GainSTM") -> timedelta:
        return self._stm_sampling_config.period()

    @property
    def sampling_config(self: "GainSTM") -> SamplingConfig:
        return self._stm_sampling_config.sampling_config()

    def _sampling_config_intensity(self: "GainSTM") -> SamplingConfig:
        return self.sampling_config

    def _sampling_config_phase(self: "GainSTM") -> SamplingConfig:
        return self.sampling_config
