import ctypes

import numpy as np

from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_def import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo

from .holo import EmissionConstraint, Holo


class Greedy(Holo):
    """Gain to produce multiple foci with greedy algorithm.

    References
    ----------
    - Suzuki, Shun, et al. "Radiation pressure field reconstruction for ultrasound midair haptics by Greedy algorithm with brute-force search,"
        IEEE Transactions on Haptics 14.4 (2021): 914-921.
    """

    _div: int

    def __init__(self: "Greedy") -> None:
        super().__init__(EmissionConstraint.uniform(EmitIntensity.maximum()))
        self._div = 16

    def with_phase_div(self: "Greedy", div: int) -> "Greedy":
        """Set parameter.

        Arguments:
        ---------
            div: parameter
        """
        self._div = div
        return self

    def phase_div(self: "Greedy") -> int:
        """Get parameter."""
        return self._div

    def _gain_ptr(self: "Greedy", _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci_ = np.ctypeslib.as_ctypes(np.array(self._foci).astype(ctypes.c_double))
        amps = np.ctypeslib.as_ctypes(np.fromiter((a.pascal for a in self._amps), dtype=float).astype(ctypes.c_double))
        return GainHolo().gain_holo_greedy(foci_, amps, size, self._div, self._constraint._constraint_ptr())
