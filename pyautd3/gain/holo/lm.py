import ctypes

import numpy as np

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import GainPtr

from .backend import Backend
from .constraint import EmissionConstraint
from .holo import HoloWithBackend


class LM(HoloWithBackend["LM"]):
    _eps1: float
    _eps2: float
    _tau: float
    _kmax: int
    _initial: np.ndarray

    def __init__(self: "LM", backend: Backend) -> None:
        super().__init__(EmissionConstraint.DontCare, backend)
        self._eps1 = 1e-8
        self._eps2 = 1e-8
        self._tau = 1e-3
        self._kmax = 5
        self._initial = np.array([])

    def with_eps1(self: "LM", eps1: float) -> "LM":
        self._eps1 = eps1
        return self

    @property
    def eps1(self: "LM") -> float:
        return self._eps1

    def with_eps2(self: "LM", eps2: float) -> "LM":
        self._eps2 = eps2
        return self

    @property
    def eps2(self: "LM") -> float:
        return self._eps2

    def with_tau(self: "LM", tau: float) -> "LM":
        self._tau = tau
        return self

    @property
    def tau(self: "LM") -> float:
        return self._tau

    def with_kmax(self: "LM", kmax: int) -> "LM":
        self._kmax = kmax
        return self

    @property
    def kmax(self: "LM") -> int:
        return self._kmax

    def with_initial(self: "LM", initial: np.ndarray) -> "LM":
        self._initial = initial
        return self

    @property
    def initial(self: "LM") -> np.ndarray:
        return self._initial

    def _gain_ptr(self: "LM", _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci_ = np.ctypeslib.as_ctypes(np.array(self._foci).astype(ctypes.c_double))
        amps = np.ctypeslib.as_ctypes(np.fromiter((a.pascal for a in self._amps), dtype=float).astype(ctypes.c_double))
        initial_ = np.ctypeslib.as_ctypes(self._initial.astype(ctypes.c_double))
        return self._backend._lm(foci_, amps, size, self._eps1, self._eps2, self._tau, self._kmax, initial_, len(self._initial), self._constraint)
