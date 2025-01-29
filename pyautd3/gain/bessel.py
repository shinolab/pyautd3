from typing import Self

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.defined.angle import Angle
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import BesselOption as BesselOption_
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Point3, Vector3


class BesselOption:
    intensity: EmitIntensity
    phase_offset: Phase

    def __init__(self: Self, *, intensity: EmitIntensity | None = None, phase_offset: Phase | None = None) -> None:
        self.intensity = intensity or EmitIntensity.maximum()
        self.phase_offset = phase_offset or Phase(0)

    def _inner(self: Self) -> BesselOption_:
        return BesselOption_(self.intensity._inner(), self.phase_offset._inner())


class Bessel(Gain):
    pos: np.ndarray
    direction: np.ndarray
    theta: Angle
    option: BesselOption

    def __init__(self: Self, pos: ArrayLike, direction: ArrayLike, theta: Angle, option: BesselOption) -> None:
        super().__init__()
        self.pos = np.array(pos)
        self.direction = np.array(direction)
        self.theta = theta
        self.option = option

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        return Base().gain_bessel(
            Point3(self.pos),
            Vector3(self.direction),
            self.theta._inner(),
            self.option._inner(),
        )
