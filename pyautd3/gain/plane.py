import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.driver.common.phase import Phase
from pyautd3.driver.datagram.gain import IGain
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import GainPtr


class Plane(IGain):
    """Gain to produce a plane wave."""

    _d: np.ndarray
    _intensity: EmitIntensity
    _phase: Phase

    def __init__(self: "Plane", direction: ArrayLike) -> None:
        """Constructor.

        Arguments:
        ---------
            direction: Direction of the plane wave
        """
        super().__init__()
        self._d = np.array(direction)
        self._intensity = EmitIntensity.maximum()
        self._phase = Phase(0)

    def dir(self: "Plane") -> np.ndarray:
        """Get direction of the plane wave."""
        return self._d

    def with_intensity(self: "Plane", intensity: int | EmitIntensity) -> "Plane":
        """Set amplitude.

        Arguments:
        ---------
            intensity: Emission intensity
        """
        self._intensity = EmitIntensity._cast(intensity)
        return self

    def intensity(self: "Plane") -> EmitIntensity:
        """Get emission intensity."""
        return self._intensity

    def with_phase(self: "Plane", phase: Phase) -> "Plane":
        """Set phase.

        Arguments:
        ---------
            phase: Phase
        """
        self._phase = phase
        return self

    def phase(self: "Plane") -> Phase:
        """Get phase."""
        return self._phase

    def _gain_ptr(self: "Plane", _: Geometry) -> GainPtr:
        return Base().gain_plane(self._d[0], self._d[1], self._d[2], self._intensity.value, self._phase.value)
