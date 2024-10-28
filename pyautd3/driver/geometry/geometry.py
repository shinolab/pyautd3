from collections.abc import Iterator
from typing import Self

import numpy as np

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GeometryPtr

from .device import Device


class Geometry:
    _geometry_ptr: GeometryPtr
    _devices: list[Device]

    def __init__(self: Self, ptr: GeometryPtr) -> None:
        self._geometry_ptr = ptr
        self._devices = [Device(i, ptr) for i in range(int(Base().geometry_num_devices(self._geometry_ptr)))]

    @property
    def center(self: Self) -> np.ndarray:
        return Base().geometr_center(self._geometry_ptr).ndarray()

    @property
    def num_devices(self: Self) -> int:
        return int(Base().geometry_num_devices(self._geometry_ptr))

    @property
    def num_transducers(self: Self) -> int:
        return int(Base().geometry_num_transducers(self._geometry_ptr))

    def __getitem__(self: Self, key: int) -> Device:
        return self._devices[key]

    def __iter__(self: Self) -> Iterator[Device]:
        return iter(self._devices)

    @property
    def devices(self: Self) -> Iterator[Device]:
        return filter(lambda x: x.enable, self._devices)

    def set_sound_speed_from_temp(
        self: Self,
        temp: float,
        k: float = 1.4,
        r: float = 8.31446261815324,
        m: float = 28.9647e-3,
    ) -> None:
        for d in self.devices:
            d.set_sound_speed_from_temp(temp, k, r, m)

    def set_sound_speed(
        self: Self,
        c: float,
    ) -> None:
        for d in self.devices:
            d.sound_speed = c
