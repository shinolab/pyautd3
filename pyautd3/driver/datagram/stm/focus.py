import ctypes
import functools
from collections.abc import Iterable
from ctypes import c_double, c_uint8

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.with_segment_transition import DatagramST, IntoDatagramWithSegmentTransition
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga import LoopBehavior
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import (
    DatagramPtr,
    FocusSTMPtr,
    SamplingConfigWrap,
    Segment,
    TransitionModeWrap,
)
from pyautd3.native_methods.autd3capi_driver import LoopBehavior as _LoopBehavior

__all__ = []  # type: ignore[var-annotated]


class ControlPoint:
    point: np.ndarray
    intensity: EmitIntensity

    def __init__(self: "ControlPoint", point: ArrayLike, intensity: EmitIntensity | None = None) -> None:
        self.point = np.array(point)
        self.intensity = EmitIntensity(0xFF) if intensity is None else intensity


class FocusSTM(
    IntoDatagramWithSegmentTransition,
    DatagramST[FocusSTMPtr],
    Datagram,
):
    _points: list[float]
    _intensities: list[EmitIntensity]

    _freq: Freq[float] | None
    _freq_nearest: Freq[float] | None
    _sampling_config: SamplingConfigWrap | None
    _loop_behavior: _LoopBehavior

    def __new__(cls: type["FocusSTM"]) -> "FocusSTM":
        raise NotImplementedError

    @classmethod
    def __private_new__(
        cls: type["FocusSTM"],
        freq: Freq[float] | None,
        freq_nearest: Freq[float] | None,
        sampling_config: SamplingConfigWrap | None,
    ) -> "FocusSTM":
        ins = super().__new__(cls)

        ins._points = []
        ins._intensities = []

        ins._freq = freq
        ins._freq_nearest = freq_nearest
        ins._sampling_config = sampling_config

        ins._loop_behavior = LoopBehavior.Infinite

        return ins

    def _raw_ptr(self: "FocusSTM", _: Geometry) -> FocusSTMPtr:
        points = np.ctypeslib.as_ctypes(np.array(self._points).astype(c_double))
        intensities = np.fromiter((i.value for i in self._intensities), dtype=c_uint8)  # type: ignore[type-var,call-overload]
        ptr: FocusSTMPtr
        if self._freq is not None:
            ptr = Base().stm_focus_from_freq(self._freq.hz)
        elif self._freq_nearest is not None:
            ptr = Base().stm_focus_from_freq_nearest(self._freq_nearest.hz)
        else:
            ptr = Base().stm_focus_from_sampling_config(self._sampling_config)  # type: ignore[arg-type]
        ptr = Base().stm_focus_with_loop_behavior(ptr, self._loop_behavior)
        return Base().stm_focus_add_foci(
            ptr,
            points,
            intensities.ctypes.data_as(ctypes.POINTER(c_uint8)),  # type: ignore[arg-type]
            len(self._intensities),
        )

    def _datagram_ptr(self: "FocusSTM", geometry: Geometry) -> DatagramPtr:
        return Base().stm_focus_into_datagram(self._raw_ptr(geometry))

    def _into_segment_transition(self: "FocusSTM", ptr: FocusSTMPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        if transition_mode is None:
            return Base().stm_focus_into_datagram_with_segment(ptr, segment)
        return Base().stm_focus_into_datagram_with_segment_transition(ptr, segment, transition_mode)

    @staticmethod
    def from_freq(freq: Freq[float]) -> "FocusSTM":
        return FocusSTM.__private_new__(freq, None, None)

    @staticmethod
    def from_freq_nearest(freq: Freq[float]) -> "FocusSTM":
        return FocusSTM.__private_new__(None, freq, None)

    @staticmethod
    def from_sampling_config(sampling_config: SamplingConfigWrap) -> "FocusSTM":
        return FocusSTM.__private_new__(None, None, sampling_config)

    def add_focus(self: "FocusSTM", point: ArrayLike | ControlPoint) -> "FocusSTM":
        p: ControlPoint
        match point:
            case ControlPoint():
                p = point
            case _:
                p = ControlPoint(point)
        self._points.append(p.point[0])
        self._points.append(p.point[1])
        self._points.append(p.point[2])
        self._intensities.append(p.intensity)
        return self

    def add_foci_from_iter(self: "FocusSTM", iterable: Iterable[ArrayLike] | Iterable[ControlPoint]) -> "FocusSTM":
        return functools.reduce(
            lambda acc, x: acc.add_focus(x),
            iterable,
            self,
        )

    def with_loop_behavior(self: "FocusSTM", value: _LoopBehavior) -> "FocusSTM":
        self._loop_behavior = value
        return self
