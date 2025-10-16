from abc import ABCMeta, abstractmethod
from typing import Self, TypeVar

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.firmware.fpga.transition_mode import FiniteTransitionMode
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3 import Segment
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, TransitionModeWrap

DL = TypeVar("DL", bound="DatagramL")
P = TypeVar("P")


class DatagramL[P](metaclass=ABCMeta):
    @abstractmethod
    def _into_loop_behavior(
        self: Self,
        ptr: P,
        segment: Segment,
        transition_mode: TransitionModeWrap,
        loop_count: int,
    ) -> DatagramPtr:
        pass

    @abstractmethod
    def _raw_ptr(self: Self, geometry: Geometry) -> P:
        pass


class WithFiniteLoop[DL: "DatagramL"](Datagram):
    inner: DL
    segment: Segment
    transition_mode: TransitionModeWrap
    loop_count: int

    def __init__(self: Self, inner: DL, segment: Segment, transition_mode: FiniteTransitionMode, loop_count: int) -> None:
        super().__init__()
        self.inner = inner
        self.segment = segment
        self.transition_mode = transition_mode._inner()
        if loop_count > 0:
            self.loop_count = loop_count
        else:
            msg = "loop_count must be greater than 0"
            raise ValueError(msg)

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return self.inner._into_loop_behavior(self.inner._raw_ptr(geometry), self.segment, self.transition_mode, self.loop_count)
