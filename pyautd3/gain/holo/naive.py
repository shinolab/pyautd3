import ctypes

import numpy as np

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_def import GainPtr

from .backend import Backend
from .holo import EmissionConstraint, HoloWithBackend


class Naive(HoloWithBackend):
    """Gain to produce multiple foci with naive linear synthesis."""

    def __init__(self: "Naive", backend: Backend) -> None:
        super().__init__(EmissionConstraint.dont_care(), backend)

    def _gain_ptr(self: "Naive", _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci_ = np.ctypeslib.as_ctypes(np.array(self._foci).astype(ctypes.c_double))
        amps = np.ctypeslib.as_ctypes(np.fromiter((a.pascal for a in self._amps), dtype=float).astype(ctypes.c_double))
        return self._backend._naive(foci_, amps, size, self._constraint)
