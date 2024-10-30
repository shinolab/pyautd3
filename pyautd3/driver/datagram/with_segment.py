from abc import ABCMeta, abstractmethod
from typing import Generic, Self, TypeVar

from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, Segment, TransitionModeWrap

__all__ = []  # type: ignore[var-annotated]

DS = TypeVar("DS", bound="DatagramS")
P = TypeVar("P")


class DatagramS(Generic[P], metaclass=ABCMeta):
    @abstractmethod
    def _into_segment(self: Self, ptr: P, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        pass

    @abstractmethod
    def _raw_ptr(self: Self, geometry: Geometry) -> P:
        pass


@datagram
class DatagramWithSegment(Datagram, Generic[DS]):
    _datagram: DS
    _segment: Segment
    _transition_mode: TransitionModeWrap | None

    def __init__(self: Self, datagram: DS, segment: Segment, transition_mode: TransitionModeWrap | None) -> None:
        self._datagram = datagram
        self._segment = segment
        self._transition_mode = transition_mode

    def _datagram_ptr(self: Self, g: Geometry) -> DatagramPtr:
        raw_ptr = self._datagram._raw_ptr(g)
        return self._datagram._into_segment(raw_ptr, self._segment, self._transition_mode)
