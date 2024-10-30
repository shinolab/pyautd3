from datetime import timedelta
from typing import Generic, Self, TypeVar

from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr

__all__ = []  # type: ignore[var-annotated]

D = TypeVar("D", bound="Datagram")


@datagram
class DatagramWithTimeout(Datagram, Generic[D]):
    _datagram: D
    _timeout: timedelta | None

    def __init__(self: Self, datagram: D, timeout: timedelta | None) -> None:
        self._datagram = datagram
        self._timeout = timeout

    def _datagram_ptr(self: Self, g: Geometry) -> DatagramPtr:
        raw_ptr = self._datagram._datagram_ptr(g)
        return Base().datagram_with_timeout(raw_ptr, int(self._timeout.total_seconds() * 1000 * 1000 * 1000) if self._timeout is not None else -1)
