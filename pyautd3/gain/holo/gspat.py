import ctypes

import numpy as np

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_def import GainPtr

from .backend import Backend
from .holo import EmissionConstraint, HoloWithBackend


class GSPAT(HoloWithBackend):
    """Gain to produce multiple foci with GS-PAT algorithm.

    Reference
    ---------
    - Plasencia, Diego Martinez, et al. "GS-PAT: high-speed multi-point sound-fields for phased arrays of transducers,"
        ACM Transactions on Graphics (TOG) 39.4 (2020): 138-1.
    """

    _repeat: int

    def __init__(self: "GSPAT", backend: Backend) -> None:
        super().__init__(EmissionConstraint.dont_care(), backend)
        self._repeat = 100

    def with_repeat(self: "GSPAT", value: int) -> "GSPAT":
        """Set parameter.

        Arguments:
        ---------
            value: parameter
        """
        self._repeat = value
        return self

    def repeat(self: "GSPAT") -> int:
        """Get parameter."""
        return self._repeat

    def _gain_ptr(self: "GSPAT", _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci_ = np.ctypeslib.as_ctypes(np.array(self._foci).astype(ctypes.c_double))
        amps = np.ctypeslib.as_ctypes(np.fromiter((a.pascal for a in self._amps), dtype=float).astype(ctypes.c_double))
        return self._backend._gspat(foci_, amps, size, self._repeat, self._constraint)
