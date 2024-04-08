import ctypes
from abc import ABCMeta, abstractmethod
from collections.abc import Callable

import numpy as np

from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr

from .datagram import Datagram

__all__ = ["DebugType", "ConfigureDebugSettings"]


class IDebugType(metaclass=ABCMeta):
    @abstractmethod
    def _ty(self: "IDebugType") -> int:
        pass

    @abstractmethod
    def _value(self: "IDebugType") -> int:
        pass


class DebugType:  # noqa: D101
    def __new__(cls: type["DebugType"]) -> "DebugType":
        """DO NOT USE THIS CONSTRUCTOR."""
        raise NotImplementedError

    class Disable(IDebugType):  # noqa: D106
        def _ty(self: "DebugType.Disable") -> int:
            return 0x00

        def _value(self: "DebugType.Disable") -> int:
            return 0x0000

    class BaseSignal(IDebugType):  # noqa: D106
        def _ty(self: "DebugType.BaseSignal") -> int:
            return 0x01

        def _value(self: "DebugType.BaseSignal") -> int:
            return 0x0000

    class Thermo(IDebugType):  # noqa: D106
        def _ty(self: "DebugType.Thermo") -> int:
            return 0x02

        def _value(self: "DebugType.Thermo") -> int:
            return 0x0000

    class ForceFan(IDebugType):  # noqa: D106
        def _ty(self: "DebugType.ForceFan") -> int:
            return 0x03

        def _value(self: "DebugType.ForceFan") -> int:
            return 0x0000

    class Sync(IDebugType):  # noqa: D106
        def _ty(self: "DebugType.Sync") -> int:
            return 0x10

        def _value(self: "DebugType.Sync") -> int:
            return 0x0000

    class ModSegment(IDebugType):  # noqa: D106
        def _ty(self: "DebugType.ModSegment") -> int:
            return 0x20

        def _value(self: "DebugType.ModSegment") -> int:
            return 0x0000

    class ModIdx(IDebugType):  # noqa: D106
        _v: int

        def __init__(self: "DebugType.ModIdx", value: int) -> None:
            super().__init__()
            self._v = value

        def _ty(self: "DebugType.ModIdx") -> int:
            return 0x21

        def _value(self: "DebugType.ModIdx") -> int:
            return self._v

    class StmSegment(IDebugType):  # noqa: D106
        def _ty(self: "DebugType.StmSegment") -> int:
            return 0x50

        def _value(self: "DebugType.StmSegment") -> int:
            return 0x0000

    class StmIdx(IDebugType):  # noqa: D106
        _v: int

        def __init__(self: "DebugType.StmIdx", value: int) -> None:
            super().__init__()
            self._v = value

        def _ty(self: "DebugType.StmIdx") -> int:
            return 0x51

        def _value(self: "DebugType.StmIdx") -> int:
            return self._v

    class IsStmMode(IDebugType):  # noqa: D106
        def _ty(self: "DebugType.IsStmMode") -> int:
            return 0x52

        def _value(self: "DebugType.IsStmMode") -> int:
            return 0x0000

    class PwmOut(IDebugType):  # noqa: D106
        _v: int

        def __init__(self: "DebugType.PwmOut", tr: Transducer) -> None:
            super().__init__()
            self._v = tr.idx

        def _ty(self: "DebugType.PwmOut") -> int:
            return 0xE0

        def _value(self: "DebugType.PwmOut") -> int:
            return self._v

    class Direct(IDebugType):  # noqa: D106
        _v: int

        def __init__(self: "DebugType.Direct", *, value: bool) -> None:
            super().__init__()
            self._v = 1 if value else 0

        def _ty(self: "DebugType.Direct") -> int:
            return 0xF0

        def _value(self: "DebugType.Direct") -> int:
            return self._v


class ConfigureDebugSettings(Datagram):  # noqa: D101
    def __init__(self: "ConfigureDebugSettings", f: Callable[[Device], list[IDebugType]]) -> None:
        super().__init__()

        self._f = f

    def _datagram_ptr(self: "ConfigureDebugSettings", geometry: Geometry) -> DatagramPtr:
        n = geometry.num_devices
        ty = np.zeros([4 * n]).astype(ctypes.c_uint8)
        value = np.zeros([4 * n]).astype(ctypes.c_uint16)
        for dev in geometry.devices:
            for i, debug_type in enumerate(self._f(dev)):
                ty[4 * dev.idx + i] = debug_type._ty()
                value[4 * dev.idx + i] = debug_type._value()
        return Base().datagram_configure_debug_settings_2(np.ctypeslib.as_ctypes(ty), np.ctypeslib.as_ctypes(value), geometry._ptr)
