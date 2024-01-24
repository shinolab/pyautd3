import ctypes

import numpy as np

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_def import GainPtr

from .backend import Backend
from .holo import EmissionConstraint, HoloWithBackend


class GS(HoloWithBackend):
    """Gain to produce multiple foci with GS algorithm.

    References
    ----------
    - Marzo, Asier, and Bruce W. Drinkwater. "Holographic acoustic tweezers,"
        Proceedings of the National Academy of Sciences 116.1 (2019): 84-89.
    """

    _repeat: int

    def __init__(self: "GS", backend: Backend) -> None:
        super().__init__(EmissionConstraint.dont_care(), backend)
        self._repeat = 100

    def with_repeat(self: "GS", value: int) -> "GS":
        """Set parameter.

        Arguments:
        ---------
            value: parameter
        """
        self._repeat = value
        return self

    def repeat(self: "GS") -> int:
        """Get parameter."""
        return self._repeat

    def _gain_ptr(self: "GS", _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci_ = np.ctypeslib.as_ctypes(np.array(self._foci).astype(ctypes.c_double))
        amps = np.ctypeslib.as_ctypes(np.fromiter((a.pascal for a in self._amps), dtype=float).astype(ctypes.c_double))
        return self._backend._gs(foci_, amps, size, self._repeat, self._constraint)
