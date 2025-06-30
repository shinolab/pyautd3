from collections.abc import Iterator
from typing import Self

import numpy as np

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import (
    DevicePtr,
    GeometryPtr,
)

from .transducer import Transducer


class Device:
    _idx: int
    _geo_ptr: GeometryPtr
    _ptr: DevicePtr
    _transducers: list[Transducer]

    def __init__(self: Self, idx: int, ptr: GeometryPtr) -> None:
        self._idx = idx
        self._geo_ptr = ptr
        self._ptr = Base().device(ptr, idx)
        self._transducers = [Transducer(i, idx, self._ptr) for i in range(int(Base().device_num_transducers(self._ptr)))]

    def idx(self: Self) -> int:
        return self._idx

    def num_transducers(self: Self) -> int:
        return len(self._transducers)

    def center(self: Self) -> np.ndarray:
        return Base().device_center(self._ptr).ndarray()

    def rotation(self: Self) -> np.ndarray:
        return Base().device_rotation(self._ptr).ndarray()

    def x_direction(self: Self) -> np.ndarray:
        return Base().device_direction_x(self._ptr).ndarray()

    def y_direction(self: Self) -> np.ndarray:
        return Base().device_direction_y(self._ptr).ndarray()

    def axial_direction(self: Self) -> np.ndarray:
        return Base().device_direction_axial(self._ptr).ndarray()

    def __getitem__(self: Self, key: int) -> Transducer:
        return self._transducers[key]

    def __iter__(self: Self) -> Iterator[Transducer]:
        return iter(self._transducers)
