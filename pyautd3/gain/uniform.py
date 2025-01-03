from typing import Self

from pyautd3.derive import datagram, gain
from pyautd3.derive.derive_builder import builder
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.drive import Drive
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr


@builder
@gain
@datagram
@datagram_with_segment
class Uniform(Gain):
    _prop_drive: Drive

    def __init__(self: Self, drive: Drive | EmitIntensity | Phase | tuple) -> None:
        super().__init__()
        self._prop_drive = Drive(drive)

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        return Base().gain_uniform(self._prop_drive.intensity.value, self._prop_drive.phase.value)
