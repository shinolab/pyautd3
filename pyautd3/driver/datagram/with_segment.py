from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_def import DatagramPtr, Segment

from .datagram import Datagram

__all__ = []  # type: ignore[var-annotated]

D = TypeVar("D", bound=Datagram)
DS = TypeVar("DS", bound="DatagramS")
P = TypeVar("P")


class DatagramWithSegment(
    Datagram,
    Generic[DS],
):
    _datagram: DS
    _segment: Segment
    _update_segment: bool

    def __init__(self: "DatagramWithSegment[DS]", datagram: DS, segment: Segment, *, update_segment: bool = True) -> None:
        self._datagram = datagram
        self._segment = segment
        self._update_segment = update_segment

    def _datagram_ptr(self: "DatagramWithSegment[DS]", geometry: Geometry) -> DatagramPtr:
        raw_ptr = self._datagram._raw_ptr(geometry)
        return self._datagram._into_segment(raw_ptr, self._segment, update_segment=self._update_segment)


class DatagramS(Datagram, Generic[DS, P], metaclass=ABCMeta):
    @abstractmethod
    def _into_segment(self: DS, ptr: P, segment: Segment, *, update_segment: bool) -> DatagramPtr:
        pass

    @abstractmethod
    def _raw_ptr(self: DS, geometry: Geometry) -> P:
        pass

    def with_segment(self: DS, segment: Segment, *, update_segment: bool = True) -> DatagramWithSegment[DS]:
        return DatagramWithSegment(self, segment, update_segment=update_segment)
