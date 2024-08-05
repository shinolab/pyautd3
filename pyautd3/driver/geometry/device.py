from collections.abc import Iterator

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import (
    DevicePtr,
    GeometryPtr,
)
from pyautd3.native_methods.structs import Quaternion, Vector3

from .transducer import Transducer


class Device:
    _idx: int
    _geo_ptr: GeometryPtr
    _ptr: DevicePtr
    _transducers: list[Transducer]

    def __init__(self: "Device", idx: int, ptr: GeometryPtr) -> None:
        self._idx = idx
        self._geo_ptr = ptr
        self._ptr = Base().device(ptr, idx)
        self._transducers = [Transducer(i, self._ptr) for i in range(int(Base().device_num_transducers(self._ptr)))]

    @property
    def idx(self: "Device") -> int:
        return self._idx

    @property
    def sound_speed(self: "Device") -> float:
        return float(Base().device_get_sound_speed(self._ptr))

    @sound_speed.setter
    def sound_speed(self: "Device", sound_speed: float) -> None:
        Base().device_set_sound_speed(self._geo_ptr, self._idx, sound_speed)

    def set_sound_speed_from_temp(
        self: "Device",
        temp: float,
        k: float = 1.4,
        r: float = 8.31446261815324,
        m: float = 28.9647e-3,
    ) -> None:
        Base().device_set_sound_speed_from_temp(self._geo_ptr, self._idx, temp, k, r, m)

    @property
    def enable(self: "Device") -> bool:
        return bool(Base().device_enable_get(self._ptr))

    @enable.setter
    def enable(self: "Device", value: bool) -> None:
        Base().device_enable_set(self._geo_ptr, self._idx, value)

    @property
    def num_transducers(self: "Device") -> int:
        return len(self._transducers)

    @property
    def center(self: "Device") -> np.ndarray:
        return Base().device_center(self._ptr).ndarray()

    def translate(self: "Device", t: ArrayLike) -> None:
        Base().device_translate(self._geo_ptr, self._idx, Vector3(np.array(t)))

    def rotate(self: "Device", r: ArrayLike) -> None:
        Base().device_rotate(self._geo_ptr, self._idx, Quaternion(np.array(r)))

    def affine(self: "Device", t: ArrayLike, r: ArrayLike) -> None:
        Base().device_affine(self._geo_ptr, self._idx, Vector3(np.array(t)), Quaternion(np.array(r)))

    @property
    def wavelength(self: "Device") -> float:
        return float(Base().device_wavelength(self._ptr))

    @property
    def wavenumber(self: "Device") -> float:
        return float(Base().device_wavenumber(self._ptr))

    @property
    def rotation(self: "Device") -> np.ndarray:
        return Base().device_rotation(self._ptr).ndarray()

    @property
    def x_direction(self: "Device") -> np.ndarray:
        return Base().device_direction_x(self._ptr).ndarray()

    @property
    def y_direction(self: "Device") -> np.ndarray:
        return Base().device_direction_y(self._ptr).ndarray()

    @property
    def axial_direction(self: "Device") -> np.ndarray:
        return Base().device_direction_axial(self._ptr).ndarray()

    def __getitem__(self: "Device", key: int) -> Transducer:
        return self._transducers[key]

    def __iter__(self: "Device") -> Iterator[Transducer]:
        return iter(self._transducers)
