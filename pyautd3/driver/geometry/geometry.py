from collections.abc import Iterator
from functools import reduce

import numpy as np

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import GeometryPtr

from .device import Device


class Geometry:
    """Geometry."""

    _ptr: GeometryPtr
    _devices: list[Device]

    def __init__(self: "Geometry", ptr: GeometryPtr) -> None:
        self._ptr = ptr
        self._devices = [Device(i, Base().device(self._ptr, i)) for i in range(int(Base().geometry_num_devices(self._ptr)))]

    @property
    def center(self: "Geometry") -> np.ndarray:
        """Get center position of all devices."""
        return reduce(
            lambda acc, x: acc + x.center,
            self._devices,
            np.zeros(3),
        ) / len(self._devices)

    @property
    def num_devices(self: "Geometry") -> int:
        """Get the number of devices."""
        return len(self._devices)

    @property
    def num_transducers(self: "Geometry") -> int:
        """Get the number of total transducers."""
        return reduce(
            lambda acc, x: acc + x.num_transducers,
            self._devices,
            0,
        )

    def __getitem__(self: "Geometry", key: int) -> Device:
        return self._devices[key]

    def __iter__(self: "Geometry") -> Iterator[Device]:
        return iter(self._devices)

    def devices(self: "Geometry") -> Iterator[Device]:
        """Get the iterator of enabled devices."""
        return filter(lambda x: x.enable, self._devices)

    def set_sound_speed_from_temp(
        self: "Geometry",
        temp: float,
        k: float = 1.4,
        r: float = 8.31446261815324,
        m: float = 28.9647e-3,
    ) -> None:
        """Set speed of sound of enabled devices from temperature.

        Arguments:
        ---------
            temp: Temperature [K]
            k: Ratio of specific heats
            r: Specific gas constant
            m: Molecular mass
        """
        for d in self.devices():
            d.set_sound_speed_from_temp(temp, k, r, m)

    def set_sound_speed(
        self: "Geometry",
        c: float,
    ) -> None:
        """Set speed of sound of enabled devices.

        Arguments:
        ---------
            c: Speed of sound [mm/s]
        """
        for d in self.devices():
            d.sound_speed = c

    def _geometry_ptr(self: "Geometry") -> GeometryPtr:
        return self._ptr
