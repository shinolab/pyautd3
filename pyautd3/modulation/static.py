from typing import Self

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.utils import _validate_u8
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr


class Static(Modulation):
    intensity: int

    def __init__(self: Self, intensity: int = 0xFF) -> None:
        super().__init__()
        self.intensity = _validate_u8(intensity)

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return Base().modulation_static(self.intensity)
