import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr


class Plane(Gain["Plane"]):
    _d: np.ndarray
    _intensity: EmitIntensity
    _phase_offset: Phase

    def __init__(self: "Plane", direction: ArrayLike) -> None:
        super().__init__()
        self._d = np.array(direction)
        self._intensity = EmitIntensity.maximum()
        self._phase_offset = Phase(0)

    @property
    def dir(self: "Plane") -> np.ndarray:
        return self._d

    def with_intensity(self: "Plane", intensity: EmitIntensity) -> "Plane":
        self._intensity = intensity
        return self

    @property
    def intensity(self: "Plane") -> EmitIntensity:
        return self._intensity

    def with_phase_offset(self: "Plane", phase: Phase) -> "Plane":
        self._phase_offset = phase
        return self

    @property
    def phase_offset(self: "Plane") -> Phase:
        return self._phase_offset

    def _gain_ptr(self: "Plane", _: Geometry) -> GainPtr:
        return Base().gain_plane(self._d[0], self._d[1], self._d[2], self._intensity.value, self._phase_offset.value)
