from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, Segment, TransitionModeWrap

from .datagram import Datagram

__all__ = []  # type: ignore[var-annotated]

DS = TypeVar("DS", bound="DatagramST")
P = TypeVar("P")


class DatagramST(Generic[P], metaclass=ABCMeta):
    @abstractmethod
    def _into_segment_transition(self: "DatagramST[P]", ptr: P, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        pass

    @abstractmethod
    def _raw_ptr(self: "DatagramST[P]", geometry: Geometry) -> P:
        pass


class DatagramWithSegmentTransition(
    IntoDatagramWithTimeout["DatagramWithSegmentTransition[DS]"],
    IntoDatagramWithParallelThreshold["DatagramWithSegmentTransition[DS]"],
    Datagram,
    Generic[DS],
):
    _datagram: DS
    _segment: Segment
    _transition_mode: TransitionModeWrap | None

    def __init__(self: "DatagramWithSegmentTransition[DS]", datagram: DS, segment: Segment, transition_mode: TransitionModeWrap | None) -> None:
        self._datagram = datagram
        self._segment = segment
        self._transition_mode = transition_mode

    def _datagram_ptr(self: "DatagramWithSegmentTransition[DS]", g: Geometry) -> DatagramPtr:
        raw_ptr = self._datagram._raw_ptr(g)
        return self._datagram._into_segment_transition(raw_ptr, self._segment, self._transition_mode)


class IntoDatagramWithSegmentTransition(DatagramST, Generic[DS]):
    def with_segment(self: DS, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegmentTransition[DS]:
        return DatagramWithSegmentTransition(self, segment, transition_mode)
