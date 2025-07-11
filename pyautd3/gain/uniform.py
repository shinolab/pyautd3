from typing import Self

from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.emit_intensity import Intensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr


class Uniform(Gain):
    intensity: Intensity
    phase: Phase

    def __init__(self: Self, intensity: Intensity, phase: Phase) -> None:
        super().__init__()
        self.intensity = intensity
        self.phase = phase

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        return Base().gain_uniform(self.intensity._inner(), self.phase._inner())
