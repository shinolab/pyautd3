import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.defined.angle import Angle
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr


class Bessel(Gain["Bessel"]):
    _p: np.ndarray
    _d: np.ndarray
    _theta: Angle
    _intensity: EmitIntensity
    _phase_offset: Phase

    def __init__(self: "Bessel", pos: ArrayLike, direction: ArrayLike, theta: Angle) -> None:
        super().__init__()
        self._p = np.array(pos)
        self._d = np.array(direction)
        self._theta = theta
        self._intensity = EmitIntensity.maximum()
        self._phase_offset = Phase(0)

    @property
    def pos(self: "Bessel") -> np.ndarray:
        return self._p

    @property
    def dir(self: "Bessel") -> np.ndarray:
        return self._d

    @property
    def theta(self: "Bessel") -> Angle:
        return self._theta

    def with_intensity(self: "Bessel", intensity: EmitIntensity) -> "Bessel":
        self._intensity = intensity
        return self

    @property
    def intensity(self: "Bessel") -> EmitIntensity:
        return self._intensity

    def with_phase_offset(self: "Bessel", phase: Phase) -> "Bessel":
        self._phase_offset = phase
        return self

    @property
    def phase_offset(self: "Bessel") -> Phase:
        return self._phase_offset

    def _gain_ptr(self: "Bessel", _: Geometry) -> GainPtr:
        return Base().gain_bessel(
            self._p[0],
            self._p[1],
            self._p[2],
            self._d[0],
            self._d[1],
            self._d[2],
            self._theta.radian,
            self._intensity.value,
            self._phase_offset.value,
        )
