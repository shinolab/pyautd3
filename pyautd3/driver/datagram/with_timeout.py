from datetime import timedelta
from typing import Generic, TypeVar

from forbiddenfruit import curse

from pyautd3.driver.datagram.datagram_tuple import DatagramTuple
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr

from .datagram import Datagram

__all__ = []  # type: ignore[var-annotated]

D = TypeVar("D", bound="Datagram")


class DatagramWithTimeout(Datagram, Generic[D]):
    _datagram: D
    _timeout: timedelta

    def __init__(self: "DatagramWithTimeout[D]", datagram: D, timeout: timedelta) -> None:
        self._datagram = datagram
        self._timeout = timeout

    def _datagram_ptr(self: "DatagramWithTimeout[D]", g: Geometry) -> DatagramPtr:
        raw_ptr = self._datagram._datagram_ptr(g)
        return Base().datagram_with_timeout(raw_ptr, int(self._timeout.total_seconds() * 1000 * 1000 * 1000))


class IntoDatagramWithTimeout(Generic[D]):
    def with_timeout(self: D, timeout: timedelta) -> DatagramWithTimeout[D]:
        return DatagramWithTimeout(self, timeout)


def __with_timeout(self: tuple[Datagram, Datagram], timeout: timedelta) -> DatagramWithTimeout[D]:
    return DatagramWithTimeout(DatagramTuple(self), timeout)


curse(tuple, "with_timeout", __with_timeout)
