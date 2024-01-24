import ctypes

import numpy as np

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_def import GainPtr

from .backend import Backend
from .holo import EmissionConstraint, HoloWithBackend


class LM(HoloWithBackend):
    """Gain to produce multiple foci with Levenberg-Marquardt algorithm.

    References
    ----------
    - Levenberg, Kenneth. "A method for the solution of certain non-linear problems in least squares,"
        Quarterly of applied mathematics 2.2 (1944): 164-168.
    - Marquardt, Donald W. "An algorithm for least-squares estimation of nonlinear parameters,"
        Journal of the society for Industrial and Applied Mathematics 11.2 (1963): 431-441.
    - K.Madsen, H.Nielsen, and O.Tingleff, “Methods for non-linear least squares problems (2nd ed.),” 2004.
    """

    _eps1: float
    _eps2: float
    _tau: float
    _kmax: int
    _initial: list[float]

    def __init__(self: "LM", backend: Backend) -> None:
        super().__init__(EmissionConstraint.dont_care(), backend)
        self._eps1 = 1e-8
        self._eps2 = 1e-8
        self._tau = 1e-3
        self._kmax = 5
        self._initial = []

    def with_eps1(self: "LM", eps1: float) -> "LM":
        """Set parameter.

        Arguments:
        ---------
            eps1: parameter
        """
        self._eps1 = eps1
        return self

    def eps1(self: "LM") -> float:
        """Get parameter."""
        return self._eps1

    def with_eps2(self: "LM", eps2: float) -> "LM":
        """Set parameter.

        Arguments:
        ---------
            eps2: parameter
        """
        self._eps2 = eps2
        return self

    def eps2(self: "LM") -> float:
        """Get parameter."""
        return self._eps2

    def with_tau(self: "LM", tau: float) -> "LM":
        """Set parameter.

        Arguments:
        ---------
            tau: parameter
        """
        self._tau = tau
        return self

    def tau(self: "LM") -> float:
        """Get parameter."""
        return self._tau

    def with_kmax(self: "LM", kmax: int) -> "LM":
        """Set parameter.

        Arguments:
        ---------
            kmax: parameter
        """
        self._kmax = kmax
        return self

    def kmax(self: "LM") -> int:
        """Get parameter."""
        return self._kmax

    def with_initial(self: "LM", initial: list[float]) -> "LM":
        """Set parameter.

        Arguments:
        ---------
            initial: parameter
        """
        self._initial = initial
        return self

    def initial(self: "LM") -> list[float]:
        """Get parameter."""
        return self._initial

    def _gain_ptr(self: "LM", _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci_ = np.ctypeslib.as_ctypes(np.array(self._foci).astype(ctypes.c_double))
        amps = np.ctypeslib.as_ctypes(np.fromiter((a.pascal for a in self._amps), dtype=float).astype(ctypes.c_double))
        initial_ = np.ctypeslib.as_ctypes(np.array(self._initial).astype(ctypes.c_double))
        return self._backend._lm(foci_, amps, size, self._eps1, self._eps2, self._tau, self._kmax, initial_, len(self._initial), self._constraint)
