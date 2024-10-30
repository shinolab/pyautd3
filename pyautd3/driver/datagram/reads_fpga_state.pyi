from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold
from collections.abc import Callable
from typing import Self
from pyautd3.driver.geometry import Device, Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr
from .datagram import Datagram



class ReadsFPGAState(Datagram):
    def __init__(self, f: Callable[[Device], bool]) -> None: ...
    def _datagram_ptr(self, geometry: Geometry) -> DatagramPtr: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[ReadsFPGAState]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[ReadsFPGAState]: ...
