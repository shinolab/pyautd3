from typing import Self

from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.drive import Drive
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr


class Uniform(Gain["Uniform"]):
    _drive: Drive

    def __init__(self: Self, drive: Drive | EmitIntensity | Phase | tuple) -> None:
        super().__init__()
        self._drive = Drive(drive)

    @property
    def drive(self: Self) -> Drive:
        return self._drive

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        return Base().gain_uniform(self._drive._intensity.value, self._drive._phase.value)
