from ctypes import Array, c_double

from pyautd3.native_methods.autd3capi_backend_cuda import (
    NativeMethods as AUTD3BackendCUDA,
)
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import EmissionConstraintWrap
from pyautd3.native_methods.utils import _validate_ptr

from .backend import Backend


class CUDABackend(Backend):
    def __init__(self: "CUDABackend") -> None:
        ptr = _validate_ptr(AUTD3BackendCUDA().cuda_backend())
        super().__init__(ptr)

    def __del__(self: "CUDABackend") -> None:
        if hasattr(self, "_ptr") and self._ptr._0 is not None:
            AUTD3BackendCUDA().cuda_backend_delete(self._ptr)
            self._ptr._0 = None

    def _sdp(
        self: "CUDABackend",
        foci: Array[c_double],
        amps: Array[c_double],
        size: int,
        alpha: float,
        lambda_: float,
        repeat: int,
        constraint: EmissionConstraintWrap,
    ) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudasdp(self._backend_ptr(), foci, amps, size, alpha, lambda_, repeat, constraint)

    def _gs(self: "CUDABackend", foci: Array[c_double], amps: Array[c_double], size: int, repeat: int, constraint: EmissionConstraintWrap) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudags(self._backend_ptr(), foci, amps, size, repeat, constraint)

    def _gspat(
        self: "CUDABackend",
        foci: Array[c_double],
        amps: Array[c_double],
        size: int,
        repeat: int,
        constraint: EmissionConstraintWrap,
    ) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudagspat(self._backend_ptr(), foci, amps, size, repeat, constraint)

    def _naive(self: "CUDABackend", foci: Array[c_double], amps: Array[c_double], size: int, constraint: EmissionConstraintWrap) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cuda_naive(self._backend_ptr(), foci, amps, size, constraint)

    def _lm(
        self: "CUDABackend",
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
        return AUTD3BackendCUDA().gain_holo_cudalm(
            self._backend_ptr(),
            foci,
            amps,
            size,
            eps1,
            eps2,
            tau,
            kmax,
            constraint,
            initial,
            initial_size,
        )
