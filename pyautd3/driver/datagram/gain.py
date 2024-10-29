from abc import ABCMeta, abstractmethod
from typing import Self

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GainPtr, Segment, TransitionModeWrap

__all__ = []  # type: ignore[var-annotated]


class Gain(
    DatagramS[GainPtr],
    Datagram,
    metaclass=ABCMeta,
):
    def __init__(self: Self) -> None:
        super().__init__()

    def _raw_ptr(self: Self, geometry: Geometry) -> GainPtr:
        return self._gain_ptr(geometry)

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        return Base().gain_into_datagram(self._gain_ptr(geometry))

    def _into_segment(self: Self, ptr: GainPtr, segment: Segment, transition_mode: TransitionModeWrap | None) -> DatagramPtr:
        return Base().gain_into_datagram_with_segment(
            ptr,
            segment,
            transition_mode if transition_mode is not None else TransitionMode.NONE,
        )

    @abstractmethod
    def _gain_ptr(self: Self, geometry: Geometry) -> GainPtr:
        pass
