import ctypes
from collections.abc import Iterable

import numpy as np

from pyautd3.driver.geometry import Geometry
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3

from .backend import Backend
from .constraint import EmissionConstraint
from .holo import HoloWithBackend


class LM(HoloWithBackend["LM"]):
    _eps1: float
    _eps2: float
    _tau: float
    _kmax: int
    _initial: np.ndarray

    def __init__(self: "LM", backend: Backend, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> None:
        super().__init__(EmissionConstraint.Clamp(0x00, 0xFF), backend, iterable)
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
        foci = np.fromiter((np.void(Vector3(d)) for d in self._foci), dtype=Vector3)  # type: ignore[type-var,call-overload]
        amps = np.fromiter((d.pascal for d in self._amps), dtype=ctypes.c_float)  # type: ignore[type-var,call-overload]
        initial_ = np.ctypeslib.as_ctypes(self._initial.astype(ctypes.c_float))
        return self._backend._lm(
            foci.ctypes.data_as(ctypes.POINTER(Vector3)),  # type: ignore[arg-type]
            amps.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
            size,
            self._eps1,
            self._eps2,
            self._tau,
            self._kmax,
            initial_,
            len(self._initial),
            self._constraint,
        )
