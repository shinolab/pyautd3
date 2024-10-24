import ctypes
from collections.abc import Iterable
from typing import Self

import numpy as np

from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.geometry import Geometry
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo
from pyautd3.native_methods.structs import Vector3

from .constraint import EmissionConstraint
from .holo import Holo


class Greedy(Holo["Greedy"]):
    _div: int

    def __init__(self: Self, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> None:
        super().__init__(EmissionConstraint.Uniform(EmitIntensity.maximum()), iterable)
        self._div = 16

    def with_phase_div(self: Self, div: int) -> Self:
        self._div = div
        return self

    @property
    def phase_div(self: Self) -> int:
        return self._div

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci = np.fromiter((np.void(Vector3(d)) for d in self._foci), dtype=Vector3)  # type: ignore[type-var,call-overload]
        amps = np.fromiter((d.pascal for d in self._amps), dtype=ctypes.c_float)  # type: ignore[type-var,call-overload]
        return GainHolo().gain_holo_greedy_sphere(
            foci.ctypes.data_as(ctypes.POINTER(Vector3)),  # type: ignore[arg-type]
            amps.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
            size,
            self._div,
            self._constraint,
        )
