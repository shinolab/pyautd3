import ctypes
from collections.abc import Iterable
from typing import Self

import numpy as np

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.datagram.stm.stm_sampling_config import FreqNearest, PeriodNearest, _sampling_config
from pyautd3.driver.datagram.with_loop_behavior import DatagramL
from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3 import GainSTMMode, Segment
from pyautd3.native_methods.autd3 import GainSTMOption as GainSTMOption_
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GainPtr, GainSTMPtr, LoopBehavior, TransitionModeWrap
from pyautd3.utils import Duration


class GainSTMOption:
    mode: GainSTMMode

    def __init__(self: Self, *, mode: GainSTMMode = GainSTMMode.PhaseIntensityFull) -> None:
        self.mode = mode

    def _inner(self: Self) -> GainSTMOption_:
        return GainSTMOption_(self.mode)


class GainSTM(DatagramS[GainSTMPtr], DatagramL[GainSTMPtr], Datagram):
    gains: list[Gain]
    config: SamplingConfig | Freq[float] | Duration | FreqNearest | PeriodNearest
    option: GainSTMOption

    @classmethod
    def __private_new__(
        cls: type["GainSTM"],
        gains: Iterable[Gain],
        config: SamplingConfig | Freq[float] | Duration | FreqNearest | PeriodNearest,
        option: GainSTMOption,
    ) -> "GainSTM":
        ins = super().__new__(cls)
        ins.gains = list(gains)
        ins.config = config
        ins.option = option
        return ins

    def __init__(
        self: Self,
        gains: Iterable[Gain],
        config: SamplingConfig | Freq[float] | Duration,
        option: GainSTMOption,
    ) -> None:
        self.gains = list(gains)
        self.config = config
        self.option = option

    def into_nearest(self: Self) -> "GainSTM":
        match self.config:
            case Freq() as freq:
                return GainSTM.__private_new__(self.gains, FreqNearest(freq), self.option)
            case Duration() as period:
                return GainSTM.__private_new__(self.gains, PeriodNearest(period), self.option)
            case _:
                raise TypeError

    def _raw_ptr(self: Self, geometry: Geometry) -> GainSTMPtr:
        gains: np.ndarray = np.ndarray(len(self.gains), dtype=GainPtr)
        for i, g in enumerate(self.gains):
            gains[i]["value"] = g._gain_ptr(geometry).value
        return Base().stm_gain(
            self.sampling_config()._inner,
            gains.ctypes.data_as(ctypes.POINTER(GainPtr)),  # type: ignore[arg-type]
            len(gains),
            self.option._inner(),
        )

    def _into_segment(
        self: Self,
        ptr: GainSTMPtr,
        segment: Segment,
        transition_mode: TransitionModeWrap | None,
    ) -> DatagramPtr:
        return Base().stm_gain_into_datagram_with_segment(ptr, segment, transition_mode or TransitionMode.NONE)

    def _into_loop_behavior(
        self: Self,
        ptr: GainSTMPtr,
        segment: Segment,
        transition_mode: TransitionModeWrap | None,
        loop_behavior: LoopBehavior,
    ) -> DatagramPtr:
        return Base().stm_gain_into_datagram_with_loop_behavior(ptr, segment, transition_mode or TransitionMode.NONE, loop_behavior)

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return Base().stm_gain_into_datagram(self._raw_ptr(geometry))

    def sampling_config(self: Self) -> SamplingConfig:
        return _sampling_config(self.config, len(self.gains))
