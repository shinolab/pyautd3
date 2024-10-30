from collections.abc import Callable
from ctypes import CFUNCTYPE
from ctypes import c_uint8
from ctypes import c_uint16
from ctypes import c_void_p
from threading import Lock
from typing import Self
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.geometry.device import Device
from pyautd3.driver.geometry.transducer import Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.native_methods.autd3capi_driver import GeometryPtr
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold



class PhaseCorrection(Datagram):
    _cache: dict[int, Callable[[Transducer], Phase]]
    _lock: Lock
    def __init__(self, f: Callable[[Device], Callable[[Transducer], Phase]]) -> None: ...
    def _datagram_ptr(self, geometry: Geometry) -> DatagramPtr: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[PhaseCorrection]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[PhaseCorrection]: ...
