import ctypes

import numpy as np

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import GainPtr

from .backend import Backend
from .constraint import EmissionConstraint
from .holo import HoloWithBackend


class SDP(HoloWithBackend["SDP"]):
    _alpha: float
    _lambda: float
    _repeat: int

    def __init__(self: "SDP", backend: Backend) -> None:
        super().__init__(EmissionConstraint.DontCare, backend)
        self._alpha = 1e-3
        self._lambda = 0.9
        self._repeat = 100

    def with_alpha(self: "SDP", alpha: float) -> "SDP":
        self._alpha = alpha
        return self

    @property
    def alpha(self: "SDP") -> float:
        return self._alpha

    def with_lambda(self: "SDP", lambda_: float) -> "SDP":
        self._lambda = lambda_
        return self

    @property
    def lambda_(self: "SDP") -> float:
        return self._lambda

    def with_repeat(self: "SDP", repeat: int) -> "SDP":
        self._repeat = repeat
        return self

    @property
    def repeat(self: "SDP") -> int:
        return self._repeat

    def _gain_ptr(self: "SDP", _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci_ = np.ctypeslib.as_ctypes(np.array(self._foci).astype(ctypes.c_double))
        amps = np.ctypeslib.as_ctypes(np.fromiter((a.pascal for a in self._amps), dtype=float).astype(ctypes.c_double))
        return self._backend._sdp(foci_, amps, size, self._alpha, self._lambda, self._repeat, self._constraint)
