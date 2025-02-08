import ctypes
from collections.abc import Iterable
from typing import Self

import numpy as np

from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.utils import _validate_nonzero_u32
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.gain.holo.backend import Backend
from pyautd3.gain.holo.constraint import EmissionConstraint
from pyautd3.gain.holo.holo import HoloWithBackend
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import EmissionConstraintWrap
from pyautd3.native_methods.autd3capi_gain_holo import GSPATOption as GSPATOption_
from pyautd3.native_methods.structs import Point3


class GSPATOption:
    repeat: int
    constraint: EmissionConstraintWrap

    def __init__(self: Self, *, repeat: int = 100, constraint: EmissionConstraintWrap | None = None) -> None:
        self.repeat = _validate_nonzero_u32(repeat)
        self.constraint = constraint or EmissionConstraint.Clamp(EmitIntensity.MIN, EmitIntensity.MAX)

    def _inner(self: Self) -> GSPATOption_:
        return GSPATOption_(self.constraint, self.repeat)


class GSPAT(HoloWithBackend["GSPAT"]):
    option: GSPATOption

    def __init__(self: Self, backend: Backend, foci: Iterable[tuple[np.ndarray, Amplitude]], option: GSPATOption) -> None:
        super().__init__(foci, backend)
        self.option = option

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        size = len(self.foci)
        points = np.fromiter((np.void(Point3(d)) for d, _ in self.foci), dtype=Point3)  # type: ignore[type-var,call-overload]
        amps = np.fromiter((d.pascal() for _, d in self.foci), dtype=ctypes.c_float)  # type: ignore[type-var,call-overload]
        return self.backend._gspat(
            points.ctypes.data_as(ctypes.POINTER(Point3)),  # type: ignore[arg-type]
            amps.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
            size,
            self.option._inner(),
        )
