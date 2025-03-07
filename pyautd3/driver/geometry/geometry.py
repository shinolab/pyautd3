import ctypes
from collections.abc import Callable, Iterator
from typing import Self

import numpy as np

from pyautd3.driver.autd3_device import AUTD3
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GeometryPtr
from pyautd3.native_methods.structs import Point3, Quaternion

from .device import Device


class Geometry:
    _geometry_ptr: GeometryPtr
    _devices: list[Device]

    def __init__(self: Self, ptr: GeometryPtr) -> None:
        self._geometry_ptr = ptr
        self._devices = [Device(i, ptr) for i in range(int(Base().geometry_num_devices(self._geometry_ptr)))]

    def center(self: Self) -> np.ndarray:
        return Base().geometr_center(self._geometry_ptr).ndarray()

    def num_devices(self: Self) -> int:
        return int(Base().geometry_num_devices(self._geometry_ptr))

    def num_transducers(self: Self) -> int:
        return int(Base().geometry_num_transducers(self._geometry_ptr))

    def __getitem__(self: Self, key: int) -> Device:
        return self._devices[key]

    def __iter__(self: Self) -> Iterator[Device]:
        return iter(self._devices)

    def devices(self: Self) -> Iterator[Device]:
        return filter(lambda x: x.enable, self._devices)

    def set_sound_speed_from_temp(
        self: Self,
        temp: float,
        k: float = 1.4,
        r: float = 8.31446261815324,
        m: float = 28.9647e-3,
    ) -> None:
        for d in self.devices():
            d.set_sound_speed_from_temp(temp, k, r, m)

    def set_sound_speed(
        self: Self,
        c: float,
    ) -> None:
        for d in self.devices():
            d.sound_speed = c

    def reconfigure(self: Self, f: Callable[[Device], AUTD3]) -> None:
        devices = [f(d) for d in self._devices]
        pos = np.fromiter((np.void(Point3(d.pos)) for d in devices), dtype=Point3)  # type: ignore[type-var,call-overload]
        rot = np.fromiter((np.void(Quaternion(d.rot)) for d in devices), dtype=Quaternion)  # type: ignore[type-var,call-overload]
        Base().geometry_reconfigure(
            self._geometry_ptr,
            pos.ctypes.data_as(ctypes.POINTER(Point3)),  # type: ignore[arg-type]
            rot.ctypes.data_as(ctypes.POINTER(Quaternion)),  # type: ignore[arg-type]
        )
        self._devices = [Device(i, self._geometry_ptr) for i in range(int(Base().geometry_num_devices(self._geometry_ptr)))]
