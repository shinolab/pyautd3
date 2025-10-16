from abc import ABCMeta, abstractmethod
from typing import Self, TypeVar

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.firmware.fpga.transition_mode import InfiniteTransitionMode
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3 import Segment
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, TransitionModeWrap

DS = TypeVar("DS", bound="DatagramS")
P = TypeVar("P")


class DatagramS[P](metaclass=ABCMeta):
    @abstractmethod
    def _into_segment(self: Self, ptr: P, segment: Segment, transition_mode: TransitionModeWrap) -> DatagramPtr:
        pass

    @abstractmethod
    def _raw_ptr(self: Self, geometry: Geometry) -> P:
        pass


class WithSegment[DS: "DatagramS"](Datagram):
    inner: DS
    segment: Segment
    transitiom_mode: TransitionModeWrap

    def __init__(self: Self, inner: DS, segment: Segment, transition_mode: InfiniteTransitionMode) -> None:
        super().__init__()
        self.inner = inner
        self.segment = segment
        self.transitiom_mode = transition_mode._inner()

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return self.inner._into_segment(self.inner._raw_ptr(geometry), self.segment, self.transitiom_mode)
