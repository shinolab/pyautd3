from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_def import DatagramPtr, Segment

from .datagram import Datagram

__all__ = []  # type: ignore[var-annotated]

DS = TypeVar("DS", bound="DatagramS")
P = TypeVar("P")


class DatagramS(Datagram, Generic[P], metaclass=ABCMeta):
    @abstractmethod
    def _into_segment(self: "DatagramS[P]", ptr: P, segment: tuple[Segment, bool] | None) -> DatagramPtr:
        pass

    @abstractmethod
    def _raw_ptr(self: "DatagramS[P]", geometry: Geometry) -> P:
        pass

    def _datagram_ptr(self: "DatagramS[P]", geometry: Geometry) -> DatagramPtr:
        return self._into_segment(self._raw_ptr(geometry), None)


class DatagramWithSegment(Datagram, Generic[DS]):
    _datagram: DS
    _segment: Segment
    _update_segment: bool

    def __init__(self: "DatagramWithSegment[DS]", datagram: DS, segment: Segment, *, update_segment: bool = True) -> None:
        self._datagram = datagram
        self._segment = segment
        self._update_segment = update_segment

    def _datagram_ptr(self: "DatagramWithSegment[DS]", g: Geometry) -> DatagramPtr:
        raw_ptr = self._datagram._raw_ptr(g)
        return self._datagram._into_segment(raw_ptr, (self._segment, self._update_segment))


class IntoDatagramWithSegment(DatagramS, Generic[DS]):
    def with_segment(self: DS, segment: Segment, *, update_segment: bool = True) -> DatagramWithSegment[DS]:
        return DatagramWithSegment(self, segment, update_segment=update_segment)
