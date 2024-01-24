import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.driver.datagram.gain import IGain
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import GainPtr


class Bessel(IGain):
    """Gain to produce a Bessel beam."""

    _p: np.ndarray
    _d: np.ndarray
    _theta: float
    _intensity: EmitIntensity

    def __init__(self: "Bessel", pos: ArrayLike, direction: ArrayLike, theta: float) -> None:
        """Constructor.

        Arguments:
        ---------
            pos: Start point of the beam (the apex of the conical wavefront of the beam)
            direction: Direction of the beam
            theta: Angle between the conical wavefront of the beam and the plane normal to `dir`
        """
        super().__init__()
        self._p = np.array(pos)
        self._d = np.array(direction)
        self._theta = theta
        self._intensity = EmitIntensity.maximum()

    def pos(self: "Bessel") -> np.ndarray:
        """Get start point of the beam."""
        return self._p

    def dir(self: "Bessel") -> np.ndarray:
        """Get direction of the beam."""
        return self._d

    def theta(self: "Bessel") -> float:
        """Get angle between the conical wavefront of the beam and the plane normal to `dir`."""
        return self._theta

    def with_intensity(self: "Bessel", intensity: int | EmitIntensity) -> "Bessel":
        """Set amplitude.

        Arguments:
        ---------
            intensity: Emission intensity
        """
        self._intensity = EmitIntensity._cast(intensity)
        return self

    def intensity(self: "Bessel") -> EmitIntensity:
        """Get emission intensity."""
        return self._intensity

    def _gain_ptr(self: "Bessel", _: Geometry) -> GainPtr:
        return Base().gain_bessel(
            self._p[0],
            self._p[1],
            self._p[2],
            self._d[0],
            self._d[1],
            self._d[2],
            self._theta,
            self._intensity.value,
        )
