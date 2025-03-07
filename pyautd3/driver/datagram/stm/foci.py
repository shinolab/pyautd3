import ctypes
from collections.abc import Iterable
from typing import Self

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.stm.control_point import (
    ControlPoint,
    ControlPoints,
    ControlPoints1,
    ControlPoints2,
    ControlPoints3,
    ControlPoints4,
    ControlPoints5,
    ControlPoints6,
    ControlPoints7,
    ControlPoints8,
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


class FociSTM(DatagramS[FociSTMPtr], DatagramL[FociSTMPtr], Datagram):
    foci: list[ControlPoints]
    config: SamplingConfig | Freq[float] | Duration | FreqNearest | PeriodNearest

    @classmethod
    def __private_new__(
        cls: type["FociSTM"],
        foci: (Iterable[ArrayLike] | Iterable[ControlPoint] | Iterable[ControlPoints]),
        config: SamplingConfig | Freq[float] | Duration | FreqNearest | PeriodNearest,
    ) -> "FociSTM":
        ins = super().__new__(cls)
        ins.__private_init__(foci, config)
        return ins

    def __private_init__(
        self: "FociSTM",
        foci: (Iterable[ArrayLike] | Iterable[ControlPoint] | Iterable[ControlPoints]),
        config: SamplingConfig | Freq[float] | Duration | FreqNearest | PeriodNearest,
    ) -> None:
        foci_ = list(foci)
        match foci_[0]:
            case ControlPoints():
                self.foci = foci_  # type: ignore[assignment]
            case ControlPoint():
                self.foci = [ControlPoints(points=[p]) for p in foci_]  # type: ignore[list-item, arg-type]
            case _:
                self.foci = [ControlPoints(points=[ControlPoint(point=p)]) for p in foci_]  # type: ignore[arg-type]

        self.config = config

    def __init__(
        self: "FociSTM",
        foci: (Iterable[ArrayLike] | Iterable[ControlPoint] | Iterable[ControlPoints]),
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
        n = self._n()
        match n:
            case 1:
                foci = (ControlPoints1(p.points[0], p.intensity.value) for p in self.foci)
            case 2:
                foci = (ControlPoints2(p.points[0], p.points[1], p.intensity.value) for p in self.foci)  # type: ignore[misc]
            case 3:
                foci = (ControlPoints3(p.points[0], p.points[1], p.points[2], p.intensity.value) for p in self.foci)  # type: ignore[misc]
            case 4:
                foci = (ControlPoints4(p.points[0], p.points[1], p.points[2], p.points[3], p.intensity.value) for p in self.foci)  # type: ignore[misc]
            case 5:
                foci = (ControlPoints5(p.points[0], p.points[1], p.points[2], p.points[3], p.points[4], p.intensity.value) for p in self.foci)  # type: ignore[misc]
            case 6:
                foci = (
                    ControlPoints6(p.points[0], p.points[1], p.points[2], p.points[3], p.points[4], p.points[5], p.intensity.value)  # type: ignore[misc]
                    for p in self.foci
                )
            case 7:
                foci = (
                    ControlPoints7(p.points[0], p.points[1], p.points[2], p.points[3], p.points[4], p.points[5], p.points[6], p.intensity.value)  # type: ignore[misc]
                    for p in self.foci
                )
            case _:
                foci = (
                    ControlPoints8(  # type: ignore[misc]
                        p.points[0],
                        p.points[1],
                        p.points[2],
                        p.points[3],
                        p.points[4],
                        p.points[5],
                        p.points[6],
                        p.points[7],
                        p.intensity.value,
                    )
                    for p in self.foci
                )
        foci_ = np.fromiter((np.void(p) for p in foci), dtype=np.dtype((np.void, 4 + n * 16)))  # type: ignore[type-var,call-overload]
        return Base().stm_foci(
            self.sampling_config()._inner,
            foci_.ctypes.data_as(ctypes.c_void_p),  # type: ignore[arg-type]
            len(self.foci),
            n,
        )

    def _into_segment(self: Self, ptr: FociSTMPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        return Base().stm_foci_into_datagram_with_segment(ptr, self._n(), segment, transition_mode or TransitionMode.NONE)

    def _into_loop_behavior(
        self: Self,
        ptr: FociSTMPtr,
        segment: Segment,
        transition_mode: TransitionModeWrap | None,
        loop_behavior: LoopBehavior,
    ) -> DatagramPtr:
        return Base().stm_foci_into_datagram_with_loop_behavior(
            ptr,
            self._n(),
            segment,
            transition_mode or TransitionMode.NONE,
            loop_behavior,
        )

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return Base().stm_foci_into_datagram(self._raw_ptr(geometry), self._n())

    def sampling_config(self: Self) -> SamplingConfig:
        return _sampling_config(self.config, len(self.foci))

    def _n(self: Self) -> int:
        n = len(self.foci[0].points)
        if any(len(f.points) != n for f in self.foci):
            msg = "All components must have the same number of foci"
            raise ValueError(msg)
        match n:
            case v if 0 < v <= 8:  # noqa: PLR2004
                return n
            case _:
                raise ValueError
