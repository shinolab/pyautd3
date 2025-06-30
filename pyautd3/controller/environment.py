from typing import Self

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import EnvironmentPtr


class Environment:
    _ptr: EnvironmentPtr

    def __init__(self: Self, ptr: EnvironmentPtr) -> None:
        self._ptr = ptr

    @property
    def sound_speed(self: Self) -> float:
        return float(Base().environment_get_sound_speed(self._ptr))

    @sound_speed.setter
    def sound_speed(self: Self, sound_speed: float) -> None:
        Base().environment_set_sound_speed(self._ptr, sound_speed)

    def set_sound_speed_from_temp(
        self: Self,
        temp: float,
        k: float = 1.4,
        r: float = 8.31446261815324,
        m: float = 28.9647e-3,
    ) -> None:
        Base().environment_set_sound_speed_from_temp(self._ptr, temp, k, r, m)

    def wavelength(self: Self) -> float:
        return float(Base().environment_wavelength(self._ptr))

    def wavenumber(self: Self) -> float:
        return float(Base().environment_wavenumber(self._ptr))
