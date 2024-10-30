from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from typing import Self
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from .datagram import Datagram



class Clear(Datagram):
    def __init__(self, ) -> None: ...
    def _datagram_ptr(self, _: Geometry) -> DatagramPtr: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[Clear]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[Clear]: ...
