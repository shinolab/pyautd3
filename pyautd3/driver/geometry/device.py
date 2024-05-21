from collections.abc import Iterator
from ctypes import c_double

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import (
    DevicePtr,
)

from .transducer import Transducer


class Device:
    _idx: int
    _ptr: DevicePtr
    _transducers: list[Transducer]

    def __init__(self: "Device", idx: int, ptr: DevicePtr) -> None:
        self._idx = idx
        self._ptr = ptr
        self._transducers = [Transducer(i, self._ptr) for i in range(int(Base().device_num_transducers(self._ptr)))]

    @property
    def idx(self: "Device") -> int:
        return self._idx

    @property
    def sound_speed(self: "Device") -> float:
        return float(Base().device_get_sound_speed(self._ptr))

    @sound_speed.setter
    def sound_speed(self: "Device", sound_speed: float) -> None:
        Base().device_set_sound_speed(self._ptr, sound_speed)

    def set_sound_speed_from_temp(
        self: "Device",
        temp: float,
        k: float = 1.4,
        r: float = 8.31446261815324,
        m: float = 28.9647e-3,
    ) -> None:
        Base().device_set_sound_speed_from_temp(self._ptr, temp, k, r, m)

    @property
    def attenuation(self: "Device") -> float:
        return float(Base().device_get_attenuation(self._ptr))

    @attenuation.setter
    def attenuation(self: "Device", attenuation: float) -> None:
        Base().device_set_attenuation(self._ptr, attenuation)

    @property
    def enable(self: "Device") -> bool:
        return bool(Base().device_enable_get(self._ptr))

    @enable.setter
    def enable(self: "Device", value: bool) -> None:
        Base().device_enable_set(self._ptr, value)

    @property
    def num_transducers(self: "Device") -> int:
        return len(self._transducers)

    @property
    def center(self: "Device") -> np.ndarray:
        v = np.zeros([3]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().device_center(self._ptr, vp)
        return v

    def translate(self: "Device", t: ArrayLike) -> None:
        t = np.array(t)
        Base().device_translate(self._ptr, t[0], t[1], t[2])

    def rotate(self: "Device", r: ArrayLike) -> None:
        r = np.array(r)
        Base().device_rotate(self._ptr, r[0], r[1], r[2], r[3])

    def affine(self: "Device", t: ArrayLike, r: ArrayLike) -> None:
        t = np.array(t)
        r = np.array(r)
        Base().device_affine(self._ptr, t[0], t[1], t[2], r[0], r[1], r[2], r[3])

    @property
    def wavelength(self: "Device") -> float:
        return float(Base().device_wavelength(self._ptr))

    @property
    def wavenumber(self: "Device") -> float:
        return float(Base().device_wavenumber(self._ptr))

    def __getitem__(self: "Device", key: int) -> Transducer:
        return self._transducers[key]

    def __iter__(self: "Device") -> Iterator[Transducer]:
        return iter(self._transducers)
