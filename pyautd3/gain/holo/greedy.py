import ctypes

import numpy as np

from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo

from .constraint import EmissionConstraint
from .holo import Holo


class Greedy(Holo["Greedy"]):
    _div: int

    def __init__(self: "Greedy") -> None:
        super().__init__(EmissionConstraint.Uniform(EmitIntensity.maximum()))
        self._div = 16

    def with_phase_div(self: "Greedy", div: int) -> "Greedy":
        self._div = div
        return self

    @property
    def phase_div(self: "Greedy") -> int:
        return self._div

    def _gain_ptr(self: "Greedy", _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci_ = np.ctypeslib.as_ctypes(np.array(self._foci).astype(ctypes.c_double))
        amps = np.ctypeslib.as_ctypes(np.fromiter((a.pascal for a in self._amps), dtype=float).astype(ctypes.c_double))
        return GainHolo().gain_holo_greedy_sphere(foci_, amps, size, self._div, self._constraint)
