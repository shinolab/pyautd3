from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr

from .datagram import Datagram


class Clear(Datagram):
    """Datagram for clear all data in devices."""

    def __init__(self: "Clear") -> None:
        super().__init__()

    def _datagram_ptr(self: "Clear", _: Geometry) -> DatagramPtr:
        return Base().datagram_clear()
