from typing import Self

from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr

from .datagram import Datagram


class Clear(
    IntoDatagramWithTimeout["Clear"],
    IntoDatagramWithParallelThreshold["Clear"],
    Datagram,
):
    def __init__(self: Self) -> None:
        super().__init__()

    def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
        return Base().datagram_clear()
