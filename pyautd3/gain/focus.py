import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr


class Focus(Gain["Focus"]):
    _p: np.ndarray
    _intensity: EmitIntensity
    _phase_offset: Phase

    def __init__(self: "Focus", pos: ArrayLike) -> None:
        super().__init__()
        self._p = np.array(pos)
        self._intensity = EmitIntensity.maximum()
        self._phase_offset = Phase(0)

    @property
    def pos(self: "Focus") -> np.ndarray:
        return self._p

    def with_intensity(self: "Focus", intensity: EmitIntensity) -> "Focus":
        self._intensity = intensity
        return self

    @property
    def intensity(self: "Focus") -> EmitIntensity:
        return self._intensity

    def with_phase_offset(self: "Focus", phase: Phase) -> "Focus":
        self._phase_offset = phase
        return self

    @property
    def phase_offset(self: "Focus") -> Phase:
        return self._phase_offset

    def _gain_ptr(self: "Focus", _: Geometry) -> GainPtr:
        return Base().gain_focus(
            self._p[0],
            self._p[1],
            self._p[2],
            self._intensity.value,
            self._phase_offset.value,
        )
