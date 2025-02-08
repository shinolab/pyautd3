import ctypes
from collections.abc import Iterable
from typing import Self

import numpy as np

from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.utils import _validate_nonzero_u16
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.gain.holo.constraint import EmissionConstraint
from pyautd3.gain.holo.holo import Holo
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import EmissionConstraintWrap
from pyautd3.native_methods.autd3capi_gain_holo import GreedyOption as GreedyOption_
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo
from pyautd3.native_methods.structs import Point3


class GreedyOption:
    phase_div: int
    constraint: EmissionConstraintWrap

    def __init__(self: Self, *, phase_div: int = 16, constraint: EmissionConstraintWrap | None = None) -> None:
        self.phase_div = _validate_nonzero_u16(phase_div)
        self.constraint = constraint or EmissionConstraint.Uniform(EmitIntensity.MAX)

    def _inner(self: Self) -> GreedyOption_:
        return GreedyOption_(self.constraint, self.phase_div)


class Greedy(Holo["Greedy"]):
    option: GreedyOption

    def __init__(self: Self, foci: Iterable[tuple[np.ndarray, Amplitude]], option: GreedyOption) -> None:
        super().__init__(foci)
        self.option = option

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        size = len(self.foci)
        points = np.fromiter((np.void(Point3(d)) for d, _ in self.foci), dtype=Point3)  # type: ignore[type-var,call-overload]
        amps = np.fromiter((d.pascal() for _, d in self.foci), dtype=ctypes.c_float)  # type: ignore[type-var,call-overload]
        return GainHolo().gain_holo_greedy_sphere(
            points.ctypes.data_as(ctypes.POINTER(Point3)),  # type: ignore[arg-type]
            amps.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
            size,
            self.option._inner(),
        )
