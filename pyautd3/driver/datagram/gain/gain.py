from abc import ABCMeta, abstractmethod
from typing import TypeVar

from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr, GainPtr, Segment

__all__ = []  # type: ignore[var-annotated]

G = TypeVar("G", bound="IGain")


class IGain(DatagramS["IGain", GainPtr], metaclass=ABCMeta):
    def __init__(self: "IGain") -> None:
        super().__init__()

    def _raw_ptr(self: "IGain", geometry: Geometry) -> GainPtr:
        return self._gain_ptr(geometry)

    def _into_segment(self: "IGain", ptr: GainPtr, segment: Segment, *, update_segment: bool) -> DatagramPtr:
        return Base().gain_into_datagram_with_segment(ptr, segment, update_segment)

    def _datagram_ptr(self: "IGain", geometry: Geometry) -> DatagramPtr:
        return Base().gain_into_datagram(self._raw_ptr(geometry))

    @abstractmethod
    def _gain_ptr(self: "IGain", geometry: Geometry) -> GainPtr:
        pass
