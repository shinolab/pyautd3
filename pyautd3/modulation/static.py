from typing import Self

from pyautd3.derive import datagram, modulation
from pyautd3.derive.derive_builder import builder
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.utils import _validate_u8
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr


@builder
@modulation
@datagram_with_segment
@datagram
class Static(Modulation):
    _prop_intensity: int

    def __init__(self: Self, intensity: int | None = None) -> None:
        super().__init__()
        match intensity:
            case None:
                self._prop_intensity = 0xFF
            case int():
                self._prop_intensity = _validate_u8(intensity)
            case _:
                raise TypeError

    @staticmethod
    def with_intensity(intensity: int) -> "Static":
        return Static(intensity)

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return Base().modulation_static(self._prop_intensity, self._loop_behavior)
