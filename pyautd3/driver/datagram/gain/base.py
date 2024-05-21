from abc import ABCMeta, abstractmethod

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GainPtr, Segment

__all__ = []  # type: ignore[var-annotated]


class GainBase(
    DatagramS[GainPtr],
    Datagram,
    metaclass=ABCMeta,
):
    def __init__(self: "GainBase") -> None:
        super().__init__()

    def _raw_ptr(self: "GainBase", geometry: Geometry) -> GainPtr:
        return self._gain_ptr(geometry)

    def _datagram_ptr(self: "GainBase", geometry: Geometry) -> DatagramPtr:
        return Base().gain_into_datagram(self._gain_ptr(geometry))

    def _into_segment(self: "GainBase", ptr: GainPtr, segment: Segment, *, transition: bool) -> DatagramPtr:
        return Base().gain_into_datagram_with_segment(ptr, segment, transition)

    @abstractmethod
    def _gain_ptr(self: "GainBase", geometry: Geometry) -> GainPtr:
        pass
