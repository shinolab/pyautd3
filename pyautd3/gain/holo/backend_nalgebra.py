from ctypes import Array, c_float
from typing import Self

from pyautd3.gain.holo.backend import Backend
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import GSOption, GSPATOption, LMOption, NaiveOption
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo
from pyautd3.native_methods.structs import Point3


class NalgebraBackend(Backend):
    def __init__(self: Self) -> None:
        super().__init__(GainHolo().nalgebra_backend_sphere())

    def __del__(self: Self) -> None:
        if self._ptr.value is not None:
            GainHolo().delete_nalgebra_backend_sphere(self._ptr)
            self._ptr.value = None

    def _gs(self: Self, foci: Array[Point3], amps: Array[c_float], size: int, option: GSOption) -> GainPtr:
        return GainHolo().gain_holo_gs_sphere(self._backend_ptr(), foci, amps, size, option)

    def _gspat(self: Self, foci: Array[Point3], amps: Array[c_float], size: int, option: GSPATOption) -> GainPtr:
        return GainHolo().gain_holo_gspat_sphere(self._backend_ptr(), foci, amps, size, option)

    def _naive(self: Self, foci: Array[Point3], amps: Array[c_float], size: int, option: NaiveOption) -> GainPtr:
        return GainHolo().gain_holo_naive_sphere(self._backend_ptr(), foci, amps, size, option)

    def _lm(self: Self, foci: Array[Point3], amps: Array[c_float], size: int, option: LMOption) -> GainPtr:
        return GainHolo().gain_holo_lm_sphere(self._backend_ptr(), foci, amps, size, option)
