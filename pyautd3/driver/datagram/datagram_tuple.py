from typing import Self

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr

__all__ = []  # type: ignore[var-annotated]


class DatagramTuple(Datagram):
    _d1: Datagram
    _d2: Datagram

    def __init__(self: Self, d: tuple[Datagram, Datagram]) -> None:
        self._d1, self._d2 = d

    def _datagram_ptr(self: Self, g: Geometry) -> DatagramPtr:
        return Base().datagram_tuple(self._d1._datagram_ptr(g), self._d2._datagram_ptr(g))
