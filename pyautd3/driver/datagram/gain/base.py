from abc import ABCMeta, abstractmethod

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr, GainPtr, Segment

__all__ = []  # type: ignore[var-annotated]


class GainBase(DatagramS[GainPtr], metaclass=ABCMeta):
    def __init__(self: "GainBase") -> None:
        super().__init__()

    def _raw_ptr(self: "GainBase", geometry: Geometry) -> GainPtr:
        return self._gain_ptr(geometry)

    def _into_segment(self: "GainBase", ptr: GainPtr, segment: tuple[Segment, bool] | None) -> DatagramPtr:
        if segment is None:
            return Base().gain_into_datagram(ptr)
        segment_, update_segment = segment
        return Base().gain_into_datagram_with_segment(ptr, segment_, update_segment)

    @abstractmethod
    def _gain_ptr(self: "GainBase", geometry: Geometry) -> GainPtr:
        pass


class ChangeGainSegment(Datagram):
    _segment: Segment

    def __init__(self: "ChangeGainSegment", segment: Segment) -> None:
        super().__init__()
        self._segment = segment

    def _datagram_ptr(self: "ChangeGainSegment", _: Geometry) -> DatagramPtr:
        return Base().datagram_change_gain_segment(self._segment)
