import ctypes
from collections.abc import Iterable
from typing import Generic, Self, TypeVar

import numpy as np

from pyautd3.driver.datagram.modulation.modulation import ModulationBase
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

from .cache import IntoModulationCache

M = TypeVar("M", bound=ModulationBase)


class Fir(
    IntoModulationCache["Fir[M]"],
    IntoModulationRadiationPressure["Fir[M]"],
    ModulationBase["Fir[M]"],
    Generic[M],
):
    _m: M
    _coef: np.ndarray

    def __init__(self: Self, m: M, iterable: Iterable[float]) -> None:
        self._m = m
        self._loop_behavior = m._loop_behavior
        self._coef = np.fromiter(iterable, dtype=ctypes.c_float)

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return Base().modulation_with_fir(
            self._m._modulation_ptr(),
            self._loop_behavior,
            self._coef.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
            len(self._coef),
        )


class IntoModulationFir(ModulationBase[M], Generic[M]):
    def with_fir(self: M, iterable: Iterable[float]) -> Fir[M]:
        return Fir(self, iterable)
