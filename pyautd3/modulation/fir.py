import ctypes
from collections.abc import Iterable
from typing import Generic, Self, TypeVar

import numpy as np

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

M = TypeVar("M", bound=Modulation)


class Fir(Modulation, Generic[M]):
    target: M
    coef: np.ndarray

    def __init__(self: Self, target: M, coef: Iterable[float]) -> None:
        self.target = target
        self.coef = np.fromiter(coef, dtype=ctypes.c_float)

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return Base().modulation_with_fir(
            self.target._modulation_ptr(),
            self.coef.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
            len(self.coef),
        )
