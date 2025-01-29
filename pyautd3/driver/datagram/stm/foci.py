import ctypes
from collections.abc import Iterable
from typing import Generic, Self, TypeVar

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.stm.control_point import (
    ControlPoints1,
    ControlPoints2,
    ControlPoints3,
    ControlPoints4,
    ControlPoints5,
    ControlPoints6,
    ControlPoints7,
    ControlPoints8,
    IControlPoints,
)
from pyautd3.driver.datagram.stm.stm_sampling_config import FreqNearest, PeriodNearest, _sampling_config
from pyautd3.driver.datagram.with_loop_behavior import DatagramL
from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3 import Segment
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, FociSTMPtr, LoopBehavior, TransitionModeWrap
from pyautd3.utils import Duration

__all__ = []  # type: ignore[var-annotated]

C = TypeVar("C", bound=IControlPoints)


class FociSTM(
    DatagramS[FociSTMPtr],
    DatagramL[FociSTMPtr],
    Datagram,
    Generic[C],
):
    foci: list[C]
    config: SamplingConfig | Freq[float] | Duration | FreqNearest | PeriodNearest

    @classmethod
    def __private_new__(
        cls: type["FociSTM"],
        foci: (
            Iterable[ArrayLike]
            | Iterable[ControlPoints1]
            | Iterable[ControlPoints2]
            | Iterable[ControlPoints3]
            | Iterable[ControlPoints4]
            | Iterable[ControlPoints5]
            | Iterable[ControlPoints6]
            | Iterable[ControlPoints7]
            | Iterable[ControlPoints8]
        ),
        config: SamplingConfig | Freq[float] | Duration | FreqNearest | PeriodNearest,
    ) -> "FociSTM":
        ins = super().__new__(cls)
        ins.__private_init__(foci, config)
        return ins

    def __private_init__(
        self: "FociSTM",
        foci: (
            Iterable[ArrayLike]
            | Iterable[ControlPoints1]
            | Iterable[ControlPoints2]
            | Iterable[ControlPoints3]
            | Iterable[ControlPoints4]
            | Iterable[ControlPoints5]
            | Iterable[ControlPoints6]
            | Iterable[ControlPoints7]
            | Iterable[ControlPoints8]
        ),
        config: SamplingConfig | Freq[float] | Duration | FreqNearest | PeriodNearest,
    ) -> None:
        foci = list(foci)
        match foci[0]:
            case (
                ControlPoints1()
                | ControlPoints2()
                | ControlPoints3()
                | ControlPoints4()
                | ControlPoints5()
                | ControlPoints6()
                | ControlPoints7()
                | ControlPoints8()
            ):
                self.foci = foci
            case _:
                self.foci = [ControlPoints1(points=p) for p in foci]

        self.config = config

    def __init__(
        self: "FociSTM",
        foci: (
            Iterable[ArrayLike]
            | Iterable[ControlPoints1]
            | Iterable[ControlPoints2]
            | Iterable[ControlPoints3]
            | Iterable[ControlPoints4]
            | Iterable[ControlPoints5]
            | Iterable[ControlPoints6]
            | Iterable[ControlPoints7]
            | Iterable[ControlPoints8]
        ),
        config: SamplingConfig | Freq[float] | Duration,
    ) -> None:
        self.__private_init__(foci, config)

    def into_nearest(self: Self) -> "FociSTM":
        match self.config:
            case Freq() as freq:
                return FociSTM.__private_new__(self.foci, FreqNearest(freq))  # type: ignore[arg-type]
            case Duration() as period:
                return FociSTM.__private_new__(self.foci, PeriodNearest(period))  # type: ignore[arg-type]
            case _:
                raise TypeError

    def _raw_ptr(self: Self, _: Geometry) -> FociSTMPtr:
        n = self.foci[0]._value()
        foci = np.fromiter((np.void(p) for p in self.foci), dtype=np.dtype((np.void, 4 + n * 16)))  # type: ignore[type-var,call-overload]
        return Base().stm_foci(
            self.sampling_config._inner,
            foci.ctypes.data_as(ctypes.c_void_p),  # type: ignore[arg-type]
            len(self.foci),
            n,
        )

    def _into_segment(self: Self, ptr: FociSTMPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        return Base().stm_foci_into_datagram_with_segment(ptr, self.foci[0]._value(), segment, transition_mode or TransitionMode.NONE)

    def _into_loop_behavior(
        self: Self,
        ptr: FociSTMPtr,
        segment: Segment,
        transition_mode: TransitionModeWrap | None,
        loop_behavior: LoopBehavior,
    ) -> DatagramPtr:
        return Base().stm_foci_into_datagram_with_loop_behavior(
            ptr,
            self.foci[0]._value(),
            segment,
            transition_mode or TransitionMode.NONE,
            loop_behavior,
        )

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return Base().stm_foci_into_datagram(self._raw_ptr(geometry), self.foci[0]._value())

    @property
    def sampling_config(self: Self) -> SamplingConfig:
        return _sampling_config(self.config, len(self.foci))
