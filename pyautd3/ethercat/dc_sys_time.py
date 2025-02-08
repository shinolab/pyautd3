from typing import Self

from pyautd3.native_methods.autd3 import DcSysTime as _DcSysTime
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.utils import Duration


class DcSysTime:
    _inner: _DcSysTime

    def __new__(cls: type["DcSysTime"]) -> "DcSysTime":
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["DcSysTime"], inner: _DcSysTime) -> "DcSysTime":
        ins = super().__new__(cls)
        ins._inner = inner
        return ins

    def sys_time(self: Self) -> int:
        return int(self._inner.dc_sys_time)

    @staticmethod
    def now() -> "DcSysTime":
        return DcSysTime.__private_new__(Base().dc_sys_time_now())

    def __add__(self: Self, other: Duration) -> "DcSysTime":
        sys_time = self.sys_time() + other.as_nanos()
        inner = _DcSysTime()
        inner.dc_sys_time = sys_time
        return DcSysTime.__private_new__(inner)

    def __sub__(self: Self, other: Duration) -> "DcSysTime":
        sys_time = self.sys_time() - other.as_nanos()
        inner = _DcSysTime()
        inner.dc_sys_time = sys_time
        return DcSysTime.__private_new__(inner)

    ZERO: "DcSysTime" = None  # type: ignore[assignment]


DcSysTime.ZERO = DcSysTime.__private_new__(_DcSysTime(0x00))
