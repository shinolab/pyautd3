from typing import Self

from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, Segment, TransitionModeWrap


class SwapSegment:
    def __new__(cls: type["SwapSegment"]) -> "SwapSegment":
        raise NotImplementedError

    @datagram
    class Gain(Datagram):
        _segment: Segment
        _transition_mode: TransitionModeWrap

        def __init__(self: Self, segment: Segment, transition_mode: TransitionModeWrap) -> None:
            super().__init__()
            self._segment = segment
            self._transition_mode = transition_mode

        def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_gain(self._segment, self._transition_mode)

    @datagram
    class Modulation(Datagram):
        _segment: Segment
        _transition_mode: TransitionModeWrap

        def __init__(self: Self, segment: Segment, transition_mode: TransitionModeWrap) -> None:
            super().__init__()
            self._segment = segment
            self._transition_mode = transition_mode

        def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_modulation(self._segment, self._transition_mode)

    @datagram
    class FociSTM(Datagram):
        _segment: Segment
        _transition_mode: TransitionModeWrap

        def __init__(self: Self, segment: Segment, transition_mode: TransitionModeWrap) -> None:
            super().__init__()
            self._segment = segment
            self._transition_mode = transition_mode

        def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_foci_stm(self._segment, self._transition_mode)

    @datagram
    class GainSTM(Datagram):
        _segment: Segment
        _transition_mode: TransitionModeWrap

        def __init__(self: Self, segment: Segment, transition_mode: TransitionModeWrap) -> None:
            super().__init__()
            self._segment = segment
            self._transition_mode = transition_mode

        def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_gain_stm(self._segment, self._transition_mode)
