from abc import ABCMeta, abstractmethod
from typing import Generic, Self, TypeVar

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3 import Segment
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, LoopBehavior, TransitionModeWrap

DL = TypeVar("DL", bound="DatagramL")
P = TypeVar("P")


class DatagramL(Generic[P], metaclass=ABCMeta):
    @abstractmethod
    def _into_loop_behavior(
        self: Self,
        ptr: P,
        segment: Segment,
        transition_mode: TransitionModeWrap | None,
        loop_behavior: LoopBehavior,
    ) -> DatagramPtr:
        pass

    @abstractmethod
    def _raw_ptr(self: Self, geometry: Geometry) -> P:
        pass


class WithLoopBehavior(Datagram, Generic[DL]):
    inner: DL
    segment: Segment
    transitiom_mode: TransitionModeWrap | None
    loop_behavior: LoopBehavior

    def __init__(self: Self, inner: DL, segment: Segment, transition_mode: TransitionModeWrap | None, loop_behavior: LoopBehavior) -> None:
        super().__init__()
        self.inner = inner
        self.segment = segment
        self.transitiom_mode = transition_mode
        self.loop_behavior = loop_behavior

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return self.inner._into_loop_behavior(self.inner._raw_ptr(geometry), self.segment, self.transitiom_mode, self.loop_behavior)
