import ctypes

import numpy as np

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_def import GainPtr

from .backend import Backend
from .holo import EmissionConstraint, HoloWithBackend


class SDP(HoloWithBackend):
    """Gain to produce multiple foci by solving Semi-Denfinite Programming.

    References
    ----------
    - Inoue, Seki, Yasutoshi Makino, and Hiroyuki Shinoda. "Active touch perception produced by airborne ultrasonic haptic hologram,"
        2015 IEEE World Haptics Conference (WHC). IEEE, 2015.
    """

    _alpha: float
    _lambda: float
    _repeat: int

    def __init__(self: "SDP", backend: Backend) -> None:
        super().__init__(EmissionConstraint.dont_care(), backend)
        self._alpha = 1e-3
        self._lambda = 0.9
        self._repeat = 100

    def with_alpha(self: "SDP", alpha: float) -> "SDP":
        """Set parameter.

        Arguments:
        ---------
            alpha: parameter
        """
        self._alpha = alpha
        return self

    def alpha(self: "SDP") -> float:
        """Get parameter."""
        return self._alpha

    def with_lambda(self: "SDP", lambda_: float) -> "SDP":
        """Set parameter.

        Arguments:
        ---------
            lambda_: parameter
        """
        self._lambda = lambda_
        return self

    def lambda_(self: "SDP") -> float:
        """Get parameter."""
        return self._lambda

    def with_repeat(self: "SDP", repeat: int) -> "SDP":
        """Set parameter.

        Arguments:
        ---------
            repeat: parameter
        """
        self._repeat = repeat
        return self

    def repeat(self: "SDP") -> int:
        """Get parameter."""
        return self._repeat

    def _gain_ptr(self: "SDP", _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci_ = np.ctypeslib.as_ctypes(np.array(self._foci).astype(ctypes.c_double))
        amps = np.ctypeslib.as_ctypes(np.fromiter((a.pascal for a in self._amps), dtype=float).astype(ctypes.c_double))
        return self._backend._sdp(foci_, amps, size, self._alpha, self._lambda, self._repeat, self._constraint)
