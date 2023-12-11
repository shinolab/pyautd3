"""
File: backend_cuda.py
Project: holo
Created Date: 11/12/2023
Author: Shun Suzuki
-----
Last Modified: 11/12/2023
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2023 Shun Suzuki. All rights reserved.

"""


from ctypes import Array, c_double

from pyautd3.internal.utils import _validate_ptr
from pyautd3.native_methods.autd3capi_backend_cuda import (
    NativeMethods as AUTD3BackendCUDA,
)
from pyautd3.native_methods.autd3capi_def import GainPtr

from .backend import Backend
from .constraint import EmissionConstraint


class CUDABackend(Backend):
    """Backend using CUDA."""

    def __init__(self: "CUDABackend") -> None:
        ptr = _validate_ptr(AUTD3BackendCUDA().cuda_backend())
        super().__init__(ptr)

    def __del__(self: "CUDABackend") -> None:
        if hasattr(self, "_ptr") and self._ptr._0 is not None:
            AUTD3BackendCUDA().cuda_backend_delete(self._ptr)
            self._ptr._0 = None

    def _sdp(self: "CUDABackend", foci: Array[c_double], amps: Array[c_double], size: int) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudasdp(self._backend_ptr(), foci, amps, size)

    def _sdp_with_alpha(self: "CUDABackend", ptr: GainPtr, v: float) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudasdp_with_alpha(ptr, v)

    def _sdp_with_repeat(self: "CUDABackend", ptr: GainPtr, v: int) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudasdp_with_repeat(ptr, v)

    def _sdp_with_lambda(self: "CUDABackend", ptr: GainPtr, v: float) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudasdp_with_lambda(ptr, v)

    def _sdp_with_constraint(self: "CUDABackend", ptr: GainPtr, v: EmissionConstraint) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudasdp_with_constraint(ptr, v._constraint_ptr())

    def _gs(self: "CUDABackend", foci: Array[c_double], amps: Array[c_double], size: int) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudags(self._backend_ptr(), foci, amps, size)

    def _gs_with_repeat(self: "CUDABackend", ptr: GainPtr, v: int) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudags_with_repeat(ptr, v)

    def _gs_with_constraint(self: "CUDABackend", ptr: GainPtr, v: EmissionConstraint) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudags_with_constraint(ptr, v._constraint_ptr())

    def _gspat(self: "CUDABackend", foci: Array[c_double], amps: Array[c_double], size: int) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudagspat(self._backend_ptr(), foci, amps, size)

    def _gspat_with_repeat(self: "CUDABackend", ptr: GainPtr, v: int) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudagspat_with_repeat(ptr, v)

    def _gspat_with_constraint(self: "CUDABackend", ptr: GainPtr, v: EmissionConstraint) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudagspat_with_constraint(ptr, v._constraint_ptr())

    def _naive(self: "CUDABackend", foci: Array[c_double], amps: Array[c_double], size: int) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cuda_naive(self._backend_ptr(), foci, amps, size)

    def _naive_with_constraint(self: "CUDABackend", ptr: GainPtr, v: EmissionConstraint) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cuda_naive_with_constraint(ptr, v._constraint_ptr())

    def _lm(self: "CUDABackend", foci: Array[c_double], amps: Array[c_double], size: int) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudalm(self._backend_ptr(), foci, amps, size)

    def _lm_with_eps1(self: "CUDABackend", ptr: GainPtr, v: float) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudalm_with_eps_1(ptr, v)

    def _lm_with_eps2(self: "CUDABackend", ptr: GainPtr, v: float) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudalm_with_eps_2(ptr, v)

    def _lm_with_tau(self: "CUDABackend", ptr: GainPtr, v: float) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudalm_with_tau(ptr, v)

    def _lm_with_kmax(self: "CUDABackend", ptr: GainPtr, v: int) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudalm_with_k_max(ptr, v)

    def _lm_with_initial(self: "CUDABackend", ptr: GainPtr, v: Array[c_double], size: int) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudalm_with_initial(ptr, v, size)

    def _lm_with_constraint(self: "CUDABackend", ptr: GainPtr, v: EmissionConstraint) -> GainPtr:
        return AUTD3BackendCUDA().gain_holo_cudalm_with_constraint(ptr, v._constraint_ptr())
