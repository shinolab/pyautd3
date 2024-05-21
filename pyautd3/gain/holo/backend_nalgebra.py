from ctypes import Array, c_double

from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import EmissionConstraintWrap
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo

from .backend import Backend


class NalgebraBackend(Backend):
    def __init__(self: "NalgebraBackend") -> None:
        super().__init__(GainHolo().nalgebra_backend_sphere())

    def __del__(self: "NalgebraBackend") -> None:
        if self._ptr._0 is not None:
            GainHolo().delete_nalgebra_backend_sphere(self._ptr)
            self._ptr._0 = None

    def _sdp(
        self: "NalgebraBackend",
        foci: Array[c_double],
        amps: Array[c_double],
        size: int,
        alpha: float,
        lambda_: float,
        repeat: int,
        constraint: EmissionConstraintWrap,
    ) -> GainPtr:
        return GainHolo().gain_holo_sdp_sphere(self._backend_ptr(), foci, amps, size, alpha, lambda_, repeat, constraint)

    def _gs(
        self: "NalgebraBackend",
        foci: Array[c_double],
        amps: Array[c_double],
        size: int,
        repeat: int,
        constraint: EmissionConstraintWrap,
    ) -> GainPtr:
        return GainHolo().gain_holo_gs_sphere(self._backend_ptr(), foci, amps, size, repeat, constraint)

    def _gspat(
        self: "NalgebraBackend",
        foci: Array[c_double],
        amps: Array[c_double],
        size: int,
        repeat: int,
        constraint: EmissionConstraintWrap,
    ) -> GainPtr:
        return GainHolo().gain_holo_gspat_sphere(self._backend_ptr(), foci, amps, size, repeat, constraint)

    def _naive(self: "NalgebraBackend", foci: Array[c_double], amps: Array[c_double], size: int, constraint: EmissionConstraintWrap) -> GainPtr:
        return GainHolo().gain_holo_naive_sphere(self._backend_ptr(), foci, amps, size, constraint)

    def _lm(
        self: "NalgebraBackend",
        foci: Array[c_double],
        amps: Array[c_double],
        size: int,
        eps1: float,
        eps2: float,
        tau: float,
        kmax: int,
        initial: Array[c_double],
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
