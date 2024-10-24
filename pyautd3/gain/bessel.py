from typing import Self

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.defined.angle import Angle
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3


class Bessel(Gain["Bessel"]):
    _p: np.ndarray
    _d: np.ndarray
    _theta: Angle
    _intensity: EmitIntensity
    _phase_offset: Phase

    def __init__(self: Self, pos: ArrayLike, direction: ArrayLike, theta: Angle) -> None:
        super().__init__()
        self._p = np.array(pos)
        self._d = np.array(direction)
        self._theta = theta
        self._intensity = EmitIntensity.maximum()
        self._phase_offset = Phase(0)

    @property
    def pos(self: Self) -> np.ndarray:
        return self._p

    @property
    def dir(self: Self) -> np.ndarray:
        return self._d

    @property
    def theta(self: Self) -> Angle:
        return self._theta

    def with_intensity(self: Self, intensity: int | EmitIntensity) -> Self:
        self._intensity = EmitIntensity(intensity)
        return self

    @property
    def intensity(self: Self) -> EmitIntensity:
        return self._intensity

    def with_phase_offset(self: Self, phase: int | Phase) -> Self:
        self._phase_offset = Phase(phase)
        return self

    @property
    def phase_offset(self: Self) -> Phase:
        return self._phase_offset

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        return Base().gain_bessel(
            Vector3(self._p),
            Vector3(self._d),
            self._theta.radian,
            self._intensity.value,
            self._phase_offset.value,
        )
