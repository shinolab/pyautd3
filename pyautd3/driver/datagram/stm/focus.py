import ctypes
import functools
from collections.abc import Iterable
from ctypes import c_uint8
from datetime import timedelta

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.driver.common.loop_behavior import LoopBehavior
from pyautd3.driver.common.sampling_config import SamplingConfiguration
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import (
    DatagramPtr,
    FocusSTMPtr,
    Segment,
)
from pyautd3.native_methods.utils import _validate_ptr

from .stm import _STM

__all__ = []  # type: ignore[var-annotated]


class FocusSTM(_STM, DatagramS["FocusSTM", FocusSTMPtr]):
    """FocusSTM is an STM for moving a single focal point.

    The sampling timing is determined by hardware, thus the sampling time is precise.

    FocusSTM has following restrictions:
    - The maximum number of sampling points is 65536.
    - The sampling frequency is `pyautd3.AUTD3.fpga_clk_freq()`/N, where `N` is a 32-bit unsigned integer.
    """

    _points: list[float]
    _intensities: list[EmitIntensity]

    def __init__(
        self: "FocusSTM",
        *,
        freq: float | None = None,
        period: timedelta | None = None,
        sampling_config: SamplingConfiguration | None = None,
    ) -> None:
        """Constructor.

        Arguments:
        ---------
            freq: Frequency of STM [Hz]. The frequency closest to `freq` from the possible frequencies is set.
            period: only for internal use.
            sampling_config: only for internal use.

        """
        super().__init__(freq, period, sampling_config)
        self._points = []
        self._intensities = []

    def _raw_ptr(self: "FocusSTM", _: Geometry) -> FocusSTMPtr:
        points = np.ctypeslib.as_ctypes(np.array(self._points).astype(ctypes.c_double))
        intensities = np.fromiter((i.value for i in self._intensities), dtype=c_uint8)  # type: ignore[type-var,call-overload]
        return _validate_ptr(
            Base().stm_focus(
                self._props(),
                points,
                intensities.ctypes.data_as(ctypes.POINTER(c_uint8)),  # type: ignore[arg-type]
                len(self._intensities),
            ),
        )

    def _datagram_ptr(self: "FocusSTM", geometry: Geometry) -> DatagramPtr:
        return Base().stm_focus_into_datagram(self._raw_ptr(geometry))

    def _into_segment(self: "FocusSTM", ptr: FocusSTMPtr, segment: Segment, *, update_segment: bool = True) -> DatagramPtr:
        return Base().stm_focus_into_datagram_with_segment(ptr, segment, update_segment)

    @staticmethod
    def from_freq(freq: float) -> "FocusSTM":
        """Constructor.

        Arguments:
        ---------
            freq: freq.

        """
        return FocusSTM(freq=freq)

    @staticmethod
    def from_period(period: timedelta) -> "FocusSTM":
        """Constructor.

        Arguments:
        ---------
            period: Period.

        """
        return FocusSTM(period=period)

    @staticmethod
    def from_sampling_config(config: SamplingConfiguration) -> "FocusSTM":
        """Constructor.

        Arguments:
        ---------
            config: Sampling configuration

        """
        return FocusSTM(sampling_config=config)

    def add_focus(self: "FocusSTM", point: ArrayLike, intensity: EmitIntensity | None = None) -> "FocusSTM":
        """Add focus.

        Arguments:
        ---------
            point: Focal point
            intensity: Emission intensity

        """
        point = np.array(point)
        self._points.append(point[0])
        self._points.append(point[1])
        self._points.append(point[2])
        self._intensities.append(intensity if intensity is not None else EmitIntensity(0xFF))
        return self

    def add_foci_from_iter(self: "FocusSTM", iterable: Iterable[np.ndarray] | Iterable[tuple[np.ndarray, int]]) -> "FocusSTM":
        """Add foci.

        Arguments:
        ---------
            iterable: Iterable of focal points or tuples of focal points and duty shifts.

        """
        return functools.reduce(
            lambda acc, x: acc.add_focus(x) if isinstance(x, np.ndarray) else acc.add_focus(x[0], x[1]),
            iterable,
            self,
        )

    @property
    def frequency(self: "FocusSTM") -> float:
        """Frequency [Hz]."""
        return self._frequency_from_size(len(self._intensities))

    @property
    def period(self: "FocusSTM") -> timedelta:
        """Period."""
        return self._period_from_size(len(self._intensities))

    @property
    def sampling_config(self: "FocusSTM") -> SamplingConfiguration:
        """Sampling frequency [Hz]."""
        return self._sampling_config_from_size(len(self._intensities))

    def with_loop_behavior(self: "FocusSTM", value: LoopBehavior) -> "FocusSTM":
        """Set loop behavior.

        Arguments:
        ---------
            value: LoopBehavior.

        """
        self._loop_behavior = value
        return self


class ChangeFocusSTMSegment(Datagram):
    _segment: Segment

    def __init__(self: "ChangeFocusSTMSegment", segment: Segment) -> None:
        super().__init__()
        self._segment = segment

    def _datagram_ptr(self: "ChangeFocusSTMSegment", _: Geometry) -> DatagramPtr:
        return Base().datagram_change_focus_stm_segment(self._segment)
