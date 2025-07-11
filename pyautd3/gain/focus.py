from typing import Self

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.emit_intensity import Intensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import FocusOption as FocusOption_
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Point3


class FocusOption:
    intensity: Intensity
    phase_offset: Phase

    def __init__(self: Self, *, intensity: Intensity | None = None, phase_offset: Phase | None = None) -> None:
        self.intensity = intensity or Intensity.MAX
        self.phase_offset = phase_offset or Phase(0)

    def _inner(self: Self) -> FocusOption_:
        return FocusOption_(self.intensity._inner(), self.phase_offset._inner())


class Focus(Gain):
    pos: np.ndarray
    option: FocusOption

    def __init__(self: Self, pos: ArrayLike, option: FocusOption) -> None:
        super().__init__()
        self.pos = np.array(pos)
        self.option = option

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        return Base().gain_focus(Point3(self.pos), self.option._inner())
