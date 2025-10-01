from typing import Self

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3 import Segment
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, TransitionModeWrap


class SwapSegmentGain(Datagram):
    _segment: Segment

    def __init__(self: Self, segment: Segment) -> None:
        super().__init__()
        self._segment = segment

    def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
        return Base().datagram_swap_segment_gain(self._segment)


class SwapSegmentModulation(Datagram):
    _segment: Segment
    _transition_mode: TransitionModeWrap

    def __init__(self: Self, segment: Segment, transition_mode: TransitionMode) -> None:
        super().__init__()
        self._segment = segment
        self._transition_mode = transition_mode._inner()

    def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
        return Base().datagram_swap_segment_modulation(self._segment, self._transition_mode)


class SwapSegmentFociSTM(Datagram):
    _segment: Segment
    _transition_mode: TransitionModeWrap

    def __init__(self: Self, segment: Segment, transition_mode: TransitionMode) -> None:
        super().__init__()
        self._segment = segment
        self._transition_mode = transition_mode._inner()

    def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
        return Base().datagram_swap_segment_foci_stm(self._segment, self._transition_mode)


class SwapSegmentGainSTM(Datagram):
    _segment: Segment
    _transition_mode: TransitionModeWrap

    def __init__(self: Self, segment: Segment, transition_mode: TransitionMode) -> None:
        super().__init__()
        self._segment = segment
        self._transition_mode = transition_mode._inner()

    def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
        return Base().datagram_swap_segment_gain_stm(self._segment, self._transition_mode)
