from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from abc import ABCMeta, abstractmethod
from typing import Generic, Self, TypeVar
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, Segment, TransitionModeWrap
from .datagram import Datagram

DS = TypeVar("DS", bound="DatagramS")
P = TypeVar("P")

class DatagramS(Generic[P]):
    def _into_segment(self, ptr: P, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr: ...
    def _raw_ptr(self, geometry: Geometry) -> P: ...

class DatagramWithSegment(Datagram, Generic[DS]):
    _datagram: DS
    _segment: Segment
    _transition_mode: TransitionModeWrap | None
    def __init__(self, datagram: DS, segment: Segment, transition_mode: TransitionModeWrap | None) -> None: ...
    def _datagram_ptr(self, g: Geometry) -> DatagramPtr: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[DatagramWithSegment]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[DatagramWithSegment]: ...

class IntoDatagramWithSegment(DatagramS, Generic[DS]):
    def with_segment(self, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramWithSegment[DS]: ...
