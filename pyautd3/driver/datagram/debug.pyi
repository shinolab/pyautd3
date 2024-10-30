import ctypes
from collections.abc import Callable
from typing import Self
from pyautd3.derive import datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Device
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.geometry import Transducer
from pyautd3.ethercat.dc_sys_time import DcSysTime
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.native_methods.autd3capi_driver import DebugTypeWrap
from pyautd3.native_methods.autd3capi_driver import GeometryPtr
from pyautd3.native_methods.autd3capi_driver import GPIOOut
from pyautd3.native_methods.utils import ConstantADT
from datetime import timedelta
from pyautd3.driver.datagram.with_timeout import DatagramWithTimeout
from pyautd3.driver.datagram.with_parallel_threshold import DatagramWithParallelThreshold



class DebugType():
    NONE: DebugTypeWrap
    BaseSignal: DebugTypeWrap
    Thermo: DebugTypeWrap
    ForceFan: DebugTypeWrap
    Sync: DebugTypeWrap
    ModSegment: DebugTypeWrap
    StmSegment: DebugTypeWrap
    IsStmMode: DebugTypeWrap
    def __new__(self, ) -> DebugType: ...
    @staticmethod
    def ModIdx(idx: int) -> DebugTypeWrap: ...
    @staticmethod
    def StmIdx(idx: int) -> DebugTypeWrap: ...
    @staticmethod
    def PwmOut(tr: Transducer) -> DebugTypeWrap: ...
    @staticmethod
    def Direct(value: bool) -> DebugTypeWrap: ...
    @staticmethod
    def SysTimeEq(value: DcSysTime) -> DebugTypeWrap: ...

class DebugSettings(Datagram):
    def __init__(self, f: Callable[[Device, GPIOOut], DebugTypeWrap]) -> None: ...
    def _datagram_ptr(self, geometry: Geometry) -> DatagramPtr: ...
    def with_timeout(self, timeout: timedelta | None) -> DatagramWithTimeout[DebugSettings]: ...
    def with_parallel_threshold(self, threshold: int | None) -> DatagramWithParallelThreshold[DebugSettings]: ...
