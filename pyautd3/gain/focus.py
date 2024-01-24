import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.driver.datagram.gain import IGain
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import GainPtr


class Focus(IGain):
    """Gain to produce a focal point."""

    _p: np.ndarray
    _intensity: EmitIntensity

    def __init__(self: "Focus", pos: ArrayLike) -> None:
        """Constructor.

        Arguments:
        ---------
            pos: Position of the focal point
        """
        super().__init__()
        self._p = np.array(pos)
        self._intensity = EmitIntensity.maximum()

    def pos(self: "Focus") -> np.ndarray:
        """Get position of the focal point."""
        return self._p

    def with_intensity(self: "Focus", intensity: int | EmitIntensity) -> "Focus":
        """Set amplitude.

        Arguments:
        ---------
            intensity: Emission intensity
        """
        self._intensity = EmitIntensity._cast(intensity)
        return self

    def intensity(self: "Focus") -> EmitIntensity:
        """Get emission intensity."""
        return self._intensity

    def _gain_ptr(self: "Focus", _: Geometry) -> GainPtr:
        return Base().gain_focus(self._p[0], self._p[1], self._p[2], self._intensity.value)
