import ctypes
from collections.abc import Iterable

import numpy as np

from pyautd3.driver.geometry import Geometry
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3

from .backend import Backend
from .constraint import EmissionConstraint
from .holo import HoloWithBackend


class GS(HoloWithBackend["GS"]):
    _repeat: int

    def __init__(self: "GS", backend: Backend, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> None:
        super().__init__(EmissionConstraint.Clamp(0x00, 0xFF), backend, iterable)
        self._repeat = 100

    def with_repeat(self: "GS", value: int) -> "GS":
        self._repeat = value
        return self

    @property
    def repeat(self: "GS") -> int:
        return self._repeat

    def _gain_ptr(self: "GS", _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci = np.fromiter((np.void(Vector3(d)) for d in self._foci), dtype=Vector3)  # type: ignore[type-var,call-overload]
        amps = np.fromiter((d.pascal for d in self._amps), dtype=ctypes.c_float)  # type: ignore[type-var,call-overload]
        return self._backend._gs(
            foci.ctypes.data_as(ctypes.POINTER(Vector3)),  # type: ignore[arg-type]
            amps.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
            size,
            self._repeat,
            self._constraint,
        )
