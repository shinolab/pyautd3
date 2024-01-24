from ctypes import Array, c_double

from pyautd3.native_methods.autd3capi_def import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo

from .backend import Backend
from .constraint import EmissionConstraint


class NalgebraBackend(Backend):
    """Backend using nalgebra."""

    def __init__(self: "NalgebraBackend") -> None:
        super().__init__(GainHolo().nalgebra_backend())

    def __del__(self: "NalgebraBackend") -> None:
        if self._ptr._0 is not None:
            GainHolo().delete_nalgebra_backend(self._ptr)
            self._ptr._0 = None

    def _sdp(
        self: "NalgebraBackend",
        foci: Array[c_double],
        amps: Array[c_double],
        size: int,
        alpha: float,
        lambda_: float,
        repeat: int,
        constraint: EmissionConstraint,
    ) -> GainPtr:
        return GainHolo().gain_holo_sdp(self._backend_ptr(), foci, amps, size, alpha, lambda_, repeat, constraint._constraint_ptr())

    def _gs(self: "NalgebraBackend", foci: Array[c_double], amps: Array[c_double], size: int, repeat: int, constraint: EmissionConstraint) -> GainPtr:
        return GainHolo().gain_holo_gs(self._backend_ptr(), foci, amps, size, repeat, constraint._constraint_ptr())

    def _gspat(
        self: "NalgebraBackend",
        foci: Array[c_double],
        amps: Array[c_double],
        size: int,
        repeat: int,
        constraint: EmissionConstraint,
    ) -> GainPtr:
        return GainHolo().gain_holo_gspat(self._backend_ptr(), foci, amps, size, repeat, constraint._constraint_ptr())

    def _naive(self: "NalgebraBackend", foci: Array[c_double], amps: Array[c_double], size: int, constraint: EmissionConstraint) -> GainPtr:
        return GainHolo().gain_holo_naive(self._backend_ptr(), foci, amps, size, constraint._constraint_ptr())

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
        constraint: EmissionConstraint,
    ) -> GainPtr:
        return GainHolo().gain_holo_lm(
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
            constraint._constraint_ptr(),
        )
