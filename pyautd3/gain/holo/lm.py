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
from pyautd3.native_methods.autd3capi_gain_holo import LMOption as LMOption_
from pyautd3.native_methods.structs import Point3


class LMOption:
    eps_1: float
    eps_2: float
    tau: float
    k_max: int
    initial: np.ndarray
    constraint: EmissionConstraintWrap

    def __init__(
        self: Self,
        *,
        eps_1: float = 1e-8,
        eps_2: float = 1e-8,
        tau: float = 1e-3,
        k_max: int = 5,
        initial: np.ndarray | None = None,
        constraint: EmissionConstraintWrap | None = None,
    ) -> None:
        self.eps_1 = eps_1
        self.eps_2 = eps_2
        self.tau = tau
        self.k_max = _validate_nonzero_u32(k_max)
        self.initial = initial or np.array([])
        self.constraint = constraint or EmissionConstraint.Clamp(EmitIntensity.MIN, EmitIntensity.MAX)

    def _inner(self: Self) -> LMOption_:
        initial_ = np.ctypeslib.as_ctypes(self.initial.astype(ctypes.c_float))
        return LMOption_(self.constraint, self.eps_1, self.eps_2, self.tau, self.k_max, initial_, len(self.initial))


class LM(HoloWithBackend["LM"]):
    option: LMOption

    def __init__(self: Self, backend: Backend, foci: Iterable[tuple[np.ndarray, Amplitude]], option: LMOption) -> None:
        super().__init__(foci, backend)
        self.option = option or LMOption()

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        size = len(self.foci)
        points = np.fromiter((np.void(Point3(d)) for d, _ in self.foci), dtype=Point3)  # type: ignore[type-var,call-overload]
        amps = np.fromiter((d.pascal() for _, d in self.foci), dtype=ctypes.c_float)  # type: ignore[type-var,call-overload]
        return self.backend._lm(
            points.ctypes.data_as(ctypes.POINTER(Point3)),  # type: ignore[arg-type]
            amps.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
            size,
            self.option._inner(),
        )
