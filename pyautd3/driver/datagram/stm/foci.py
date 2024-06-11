import ctypes
from collections.abc import Iterable
from typing import Generic, TypeVar

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
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_segment_transition import DatagramST, IntoDatagramWithSegmentTransition
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga import LoopBehavior
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import (
    DatagramPtr,
    FociSTMPtr,
    SamplingConfigWrap,
    Segment,
    TransitionModeWrap,
)
from pyautd3.native_methods.autd3capi_driver import LoopBehavior as _LoopBehavior
from pyautd3.native_methods.utils import _validate_ptr

__all__ = []  # type: ignore[var-annotated]

C = TypeVar("C", bound=IControlPoints)


class FociSTM(
    IntoDatagramWithTimeout["FociSTM[C]"],
    IntoDatagramWithParallelThreshold["FociSTM[C]"],
    IntoDatagramWithSegmentTransition,
    DatagramST[FociSTMPtr],
    Datagram,
    Generic[C],
):
    _points: list[C]

    _freq: Freq[float] | None
    _freq_nearest: Freq[float] | None
    _sampling_config: SamplingConfigWrap | None
    _loop_behavior: _LoopBehavior

    def __new__(cls: type["FociSTM"]) -> "FociSTM":
        raise NotImplementedError

    @classmethod
    def __private_new__(
        cls: type["FociSTM"],
        freq: Freq[float] | None,
        freq_nearest: Freq[float] | None,
        sampling_config: SamplingConfigWrap | None,
        iterable: Iterable[C],
    ) -> "FociSTM":
        ins = super().__new__(cls)

        ins._points = list(iterable)

        ins._freq = freq
        ins._freq_nearest = freq_nearest
        ins._sampling_config = sampling_config

        ins._loop_behavior = LoopBehavior.Infinite

        return ins

    def _raw_ptr(self: "FociSTM", _: Geometry) -> FociSTMPtr:
        n = self._points[0]._value()
        points = np.fromiter((np.void(p) for p in self._points), dtype=np.dtype((np.void, 4 + n * 16)))  # type: ignore[type-var,call-overload]
        ptr: FociSTMPtr
        if self._freq is not None:
            ptr = _validate_ptr(
                Base().stm_foci_from_freq(
                    self._freq.hz,
                    points.ctypes.data_as(ctypes.c_void_p),  # type: ignore[arg-type]
                    len(self._points),
                    n,
                ),
            )
        elif self._freq_nearest is not None:
            ptr = _validate_ptr(
                Base().stm_foci_from_freq_nearest(
                    self._freq_nearest.hz,
                    points.ctypes.data_as(ctypes.c_void_p),  # type: ignore[arg-type]
                    len(self._points),
                    n,
                ),
            )
        else:
            ptr = Base().stm_foci_from_sampling_config(
                self._sampling_config,  # type: ignore[arg-type]
                points.ctypes.data_as(ctypes.c_void_p),  # type: ignore[arg-type]
                len(self._points),
                n,
            )
        ptr = Base().stm_foci_with_loop_behavior(ptr, n, self._loop_behavior)
        return ptr

    def _datagram_ptr(self: "FociSTM", geometry: Geometry) -> DatagramPtr:
        return Base().stm_foci_into_datagram(self._raw_ptr(geometry), self._points[0]._value())

    def _into_segment_transition(self: "FociSTM", ptr: FociSTMPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        if transition_mode is None:
            return Base().stm_foci_into_datagram_with_segment(ptr, self._points[0]._value(), segment)
        return Base().stm_foci_into_datagram_with_segment_transition(ptr, self._points[0]._value(), segment, transition_mode)

    @staticmethod
    def from_freq(
        freq: Freq[float],
        iterable: Iterable[ArrayLike]
        | Iterable[ControlPoints1]
        | Iterable[ControlPoints2]
        | Iterable[ControlPoints3]
        | Iterable[ControlPoints4]
        | Iterable[ControlPoints5]
        | Iterable[ControlPoints6]
        | Iterable[ControlPoints7]
        | Iterable[ControlPoints8],
    ) -> "FociSTM":
        foci = list(iterable)
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
                return FociSTM.__private_new__(freq, None, None, foci)
            case _:
                return FociSTM.__private_new__(freq, None, None, (ControlPoints1(p) for p in foci))

    @staticmethod
    def from_freq_nearest(
        freq: Freq[float],
        iterable: Iterable[ArrayLike]
        | Iterable[ControlPoints1]
        | Iterable[ControlPoints2]
        | Iterable[ControlPoints3]
        | Iterable[ControlPoints4]
        | Iterable[ControlPoints5]
        | Iterable[ControlPoints6]
        | Iterable[ControlPoints7]
        | Iterable[ControlPoints8],
    ) -> "FociSTM":
        foci = list(iterable)
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
                return FociSTM.__private_new__(None, freq, None, foci)
            case _:
                return FociSTM.__private_new__(None, freq, None, (ControlPoints1(p) for p in foci))

    @staticmethod
    def from_sampling_config(
        sampling_config: SamplingConfigWrap,
        iterable: Iterable[ArrayLike]
        | Iterable[ControlPoints1]
        | Iterable[ControlPoints2]
        | Iterable[ControlPoints3]
        | Iterable[ControlPoints4]
        | Iterable[ControlPoints5]
        | Iterable[ControlPoints6]
        | Iterable[ControlPoints7]
        | Iterable[ControlPoints8],
    ) -> "FociSTM":
        foci = list(iterable)
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
                return FociSTM.__private_new__(None, None, sampling_config, foci)
            case _:
                return FociSTM.__private_new__(None, None, sampling_config, (ControlPoints1(p) for p in foci))

    def with_loop_behavior(self: "FociSTM", value: _LoopBehavior) -> "FociSTM":
        self._loop_behavior = value
        return self
