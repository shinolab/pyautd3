from datetime import timedelta
from typing import Self

from pyautd3.native_methods.autd3capi import NativeMethods as Base


class DcSysTime:
    _dc_sys_time: int

    def __new__(cls: type["DcSysTime"]) -> "DcSysTime":
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["DcSysTime"], dc_sys_time: int) -> "DcSysTime":
        ins = super().__new__(cls)
        ins._dc_sys_time = dc_sys_time
        return ins

    @property
    def sys_time(self: Self) -> int:
        return self._dc_sys_time

    @staticmethod
    def now() -> "DcSysTime":
        return DcSysTime.__private_new__(int(Base().dc_sys_time_now()))

    def __add__(self: Self, other: timedelta) -> "DcSysTime":
        return DcSysTime.__private_new__(self._dc_sys_time + int(other.total_seconds() * 1000 * 1000 * 1000))

    def __sub__(self: Self, other: "timedelta") -> "DcSysTime":
        return DcSysTime.__private_new__(self._dc_sys_time - int(other.total_seconds() * 1000 * 1000 * 1000))
