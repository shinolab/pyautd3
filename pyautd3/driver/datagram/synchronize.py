from typing import Self

from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr


@datagram
class Synchronize(Datagram):
    def __init__(self: Self) -> None:
        super().__init__()

    def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
        return Base().datagram_synchronize()
