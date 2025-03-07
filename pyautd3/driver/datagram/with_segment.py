from abc import ABCMeta, abstractmethod
from typing import Generic, Self, TypeVar

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3 import Segment
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, TransitionModeWrap

DS = TypeVar("DS", bound="DatagramS")
P = TypeVar("P")


class DatagramS(Generic[P], metaclass=ABCMeta):
    @abstractmethod
    def _into_segment(self: Self, ptr: P, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        pass

    @abstractmethod
    def _raw_ptr(self: Self, geometry: Geometry) -> P:
        pass


class WithSegment(Datagram, Generic[DS]):
    inner: DS
    segment: Segment
    transitiom_mode: TransitionModeWrap | None

    def __init__(self: Self, inner: DS, segment: Segment, transition_mode: TransitionModeWrap | None) -> None:
        super().__init__()
        self.inner = inner
        self.segment = segment
        self.transitiom_mode = transition_mode

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return self.inner._into_segment(self.inner._raw_ptr(geometry), self.segment, self.transitiom_mode)
