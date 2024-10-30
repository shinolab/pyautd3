from ctypes import Array, c_float
from typing import Self

from pyautd3.gain.holo.backend import Backend
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import EmissionConstraintWrap
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo
from pyautd3.native_methods.structs import Vector3


class NalgebraBackend(Backend):
    def __init__(self: Self) -> None:
        super().__init__(GainHolo().nalgebra_backend_sphere())

    def __del__(self: Self) -> None:
        if self._ptr._0 is not None:
            GainHolo().delete_nalgebra_backend_sphere(self._ptr)
            self._ptr._0 = None

    def _gs(
        self: Self,
        foci: Array[Vector3],
        amps: Array[c_float],
        size: int,
        repeat: int,
        constraint: EmissionConstraintWrap,
    ) -> GainPtr:
        return GainHolo().gain_holo_gs_sphere(self._backend_ptr(), foci, amps, size, repeat, constraint)

    def _gspat(
        self: Self,
        foci: Array[Vector3],
        amps: Array[c_float],
        size: int,
        repeat: int,
        constraint: EmissionConstraintWrap,
    ) -> GainPtr:
        return GainHolo().gain_holo_gspat_sphere(self._backend_ptr(), foci, amps, size, repeat, constraint)

    def _naive(self: Self, foci: Array[Vector3], amps: Array[c_float], size: int, constraint: EmissionConstraintWrap) -> GainPtr:
        return GainHolo().gain_holo_naive_sphere(self._backend_ptr(), foci, amps, size, constraint)

    def _lm(
        self: Self,
        foci: Array[Vector3],
        amps: Array[c_float],
        size: int,
        eps1: float,
        eps2: float,
        tau: float,
        kmax: int,
        initial: Array[c_float],
        initial_size: int,
        constraint: EmissionConstraintWrap,
    ) -> GainPtr:
        return GainHolo().gain_holo_lm_sphere(
            self._backend_ptr(),
            foci,
            amps,
            size,
            eps1,
            eps2,
            tau,
            kmax,
            initial,
            initial_size,
            constraint,
        )
