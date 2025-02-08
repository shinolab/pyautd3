from typing import Self

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import PlaneOption as PlaneOption_
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3


class PlaneOption:
    intensity: EmitIntensity
    phase_offset: Phase

    def __init__(self: Self, *, intensity: EmitIntensity | None = None, phase_offset: Phase | None = None) -> None:
        self.intensity = intensity or EmitIntensity.MAX
        self.phase_offset = phase_offset or Phase(0)

    def _inner(self: Self) -> PlaneOption_:
        return PlaneOption_(self.intensity._inner(), self.phase_offset._inner())


class Plane(Gain):
    direction: np.ndarray
    option: PlaneOption

    def __init__(self: Self, direction: ArrayLike, option: PlaneOption) -> None:
        super().__init__()
        self.direction = np.array(direction)
        self.option = option

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        return Base().gain_plane(Vector3(self.direction), self.option._inner())
