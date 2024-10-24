from typing import Self

from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, Segment, TransitionModeWrap

from .datagram import Datagram


class SwapSegment:
    def __new__(cls: type["SwapSegment"]) -> "SwapSegment":
        raise NotImplementedError

    class Gain(
        IntoDatagramWithTimeout["SwapSegment.Gain"],
        IntoDatagramWithParallelThreshold["SwapSegment.Gain"],
        Datagram,
    ):
        _segment: Segment
        _transition_mode: TransitionModeWrap

        def __init__(self: Self, segment: Segment, transition_mode: TransitionModeWrap) -> None:
            super().__init__()
            self._segment = segment
            self._transition_mode = transition_mode

        def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_gain(self._segment, self._transition_mode)

    class Modulation(
        IntoDatagramWithTimeout["SwapSegment.Modulation"],
        IntoDatagramWithParallelThreshold["SwapSegment.Modulation"],
        Datagram,
    ):
        _segment: Segment
        _transition_mode: TransitionModeWrap

        def __init__(self: Self, segment: Segment, transition_mode: TransitionModeWrap) -> None:
            super().__init__()
            self._segment = segment
            self._transition_mode = transition_mode

        def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_modulation(self._segment, self._transition_mode)

    class FociSTM(
        IntoDatagramWithTimeout["SwapSegment.FociSTM"],
        IntoDatagramWithParallelThreshold["SwapSegment.FociSTM"],
        Datagram,
    ):
        _segment: Segment
        _transition_mode: TransitionModeWrap

        def __init__(self: Self, segment: Segment, transition_mode: TransitionModeWrap) -> None:
            super().__init__()
            self._segment = segment
            self._transition_mode = transition_mode

        def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_foci_stm(self._segment, self._transition_mode)

    class GainSTM(
        IntoDatagramWithTimeout["SwapSegment.GainSTM"],
        IntoDatagramWithParallelThreshold["SwapSegment.GainSTM"],
        Datagram,
    ):
        _segment: Segment
        _transition_mode: TransitionModeWrap

        def __init__(self: Self, segment: Segment, transition_mode: TransitionModeWrap) -> None:
            super().__init__()
            self._segment = segment
            self._transition_mode = transition_mode

        def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_gain_stm(self._segment, self._transition_mode)
