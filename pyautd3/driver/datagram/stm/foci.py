import ctypes
from collections.abc import Iterable
from datetime import timedelta
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
    FociSTMPtr,
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

    _stm_sampling_config: STMSamplingConfig
    _loop_behavior: _LoopBehavior

    def __private_init__(
        self: "FociSTM",
        sampling_config: STMSamplingConfig,
        foci: list[ArrayLike]
        | list[ControlPoints1]
        | list[ControlPoints2]
        | list[ControlPoints3]
        | list[ControlPoints4]
        | list[ControlPoints5]
        | list[ControlPoints6]
        | list[ControlPoints7]
        | list[ControlPoints8],
    ) -> None:
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
                self._points = foci
            case _:
                self._points = [ControlPoints1(p) for p in foci]

        self._stm_sampling_config = sampling_config

        self._loop_behavior = LoopBehavior.Infinite

    def __init__(
        self: "FociSTM",
        config: "SamplingConfig | Freq[float] | timedelta",
        iterable: Iterable[ArrayLike]
        | Iterable[ControlPoints1]
        | Iterable[ControlPoints2]
        | Iterable[ControlPoints3]
        | Iterable[ControlPoints4]
        | Iterable[ControlPoints5]
        | Iterable[ControlPoints6]
        | Iterable[ControlPoints7]
        | Iterable[ControlPoints8],
    ) -> None:
        foci = list(iterable)
        self.__private_init__(STMSamplingConfig(config, len(foci)), foci)

    @classmethod
    def nearest(
        cls: type["FociSTM"],
        config: "Freq[float] | timedelta",
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
        ins = cls.__new__(cls)
        foci = list(iterable)
        ins.__private_init__(STMSamplingConfig._nearest(config, len(foci)), foci)
        return ins

    def _raw_ptr(self: "FociSTM", _: Geometry) -> FociSTMPtr:
        return self._ptr()

    def _ptr(self: "FociSTM") -> FociSTMPtr:
        n = self._points[0]._value()
        points = np.fromiter((np.void(p) for p in self._points), dtype=np.dtype((np.void, 4 + n * 16)))  # type: ignore[type-var,call-overload]
        ptr: FociSTMPtr = _validate_ptr(
            Base().stm_foci(
                self._stm_sampling_config._inner,
                points.ctypes.data_as(ctypes.c_void_p),  # type: ignore[arg-type]
                len(self._points),
                n,
            ),
        )
        return Base().stm_foci_with_loop_behavior(ptr, n, self._loop_behavior)

    def _datagram_ptr(self: "FociSTM", geometry: Geometry) -> DatagramPtr:
        return Base().stm_foci_into_datagram(self._raw_ptr(geometry), self._points[0]._value())

    def _into_segment_transition(self: "FociSTM", ptr: FociSTMPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        if transition_mode is None:
            return Base().stm_foci_into_datagram_with_segment(ptr, self._points[0]._value(), segment)
        return Base().stm_foci_into_datagram_with_segment_transition(ptr, self._points[0]._value(), segment, transition_mode)

    def with_loop_behavior(self: "FociSTM", value: _LoopBehavior) -> "FociSTM":
        self._loop_behavior = value
        return self

    @property
    def freq(self: "FociSTM") -> Freq[float]:
        return self._stm_sampling_config.freq()

    @property
    def period(self: "FociSTM") -> timedelta:
        return self._stm_sampling_config.period()

    @property
    def sampling_config(self: "FociSTM") -> SamplingConfig:
        return self._stm_sampling_config.sampling_config()

    def _sampling_config_intensity(self: "FociSTM") -> SamplingConfig:
        return self.sampling_config

    def _sampling_config_phase(self: "FociSTM") -> SamplingConfig:
        return self.sampling_config
