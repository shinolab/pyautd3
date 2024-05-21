from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, Segment, TransitionModeWrap

from .datagram import Datagram


class SwapSegment:
    def __new__(cls: type["SwapSegment"]) -> "SwapSegment":
        raise NotImplementedError

    class _Gain(Datagram):
        _segment: Segment

        def __new__(cls: type["SwapSegment._Gain"]) -> "SwapSegment._Gain":
            raise NotImplementedError

        @classmethod
        def __private_new__(cls: type["SwapSegment._Gain"], segment: Segment) -> "SwapSegment._Gain":
            ins = super().__new__(cls)
            ins._segment = segment
            return ins

        def _datagram_ptr(self: "SwapSegment._Gain", _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_gain(segment=self._segment)

    class _Modulation(Datagram):
        _segment: Segment
        _transition_mode: TransitionModeWrap

        def __new__(cls: type["SwapSegment._Modulation"]) -> "SwapSegment._Modulation":
            raise NotImplementedError

        @classmethod
        def __private_new__(cls: type["SwapSegment._Modulation"], segment: Segment, transition_mode: TransitionModeWrap) -> "SwapSegment._Modulation":
            ins = super().__new__(cls)
            ins._segment = segment
            ins._transition_mode = transition_mode
            return ins

        def _datagram_ptr(self: "SwapSegment._Modulation", _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_modulation(self._segment, self._transition_mode)

    class _FocusSTM(Datagram):
        _segment: Segment
        _transition_mode: TransitionModeWrap

        def __new__(cls: type["SwapSegment._FocusSTM"]) -> "SwapSegment._FocusSTM":
            raise NotImplementedError

        @classmethod
        def __private_new__(cls: type["SwapSegment._FocusSTM"], segment: Segment, transition_mode: TransitionModeWrap) -> "SwapSegment._FocusSTM":
            ins = super().__new__(cls)
            ins._segment = segment
            ins._transition_mode = transition_mode
            return ins

        def _datagram_ptr(self: "SwapSegment._FocusSTM", _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_focus_stm(self._segment, self._transition_mode)

    class _GainSTM(Datagram):
        _segment: Segment
        _transition_mode: TransitionModeWrap

        def __new__(cls: type["SwapSegment._GainSTM"]) -> "SwapSegment._GainSTM":
            raise NotImplementedError

        @classmethod
        def __private_new__(cls: type["SwapSegment._GainSTM"], segment: Segment, transition_mode: TransitionModeWrap) -> "SwapSegment._GainSTM":
            ins = super().__new__(cls)
            ins._segment = segment
            ins._transition_mode = transition_mode
            return ins

        def _datagram_ptr(self: "SwapSegment._GainSTM", _: Geometry) -> DatagramPtr:
            return Base().datagram_swap_segment_gain_stm(self._segment, self._transition_mode)

    @staticmethod
    def gain(segment: Segment) -> "SwapSegment._Gain":
        return SwapSegment._Gain.__private_new__(segment)

    @staticmethod
    def modulation(segment: Segment, transition_mode: TransitionModeWrap) -> "SwapSegment._Modulation":
        return SwapSegment._Modulation.__private_new__(segment, transition_mode)

    @staticmethod
    def focus_stm(segment: Segment, transition_mode: TransitionModeWrap) -> "SwapSegment._FocusSTM":
        return SwapSegment._FocusSTM.__private_new__(segment, transition_mode)

    @staticmethod
    def gain_stm(segment: Segment, transition_mode: TransitionModeWrap) -> "SwapSegment._GainSTM":
        return SwapSegment._GainSTM.__private_new__(segment, transition_mode)
