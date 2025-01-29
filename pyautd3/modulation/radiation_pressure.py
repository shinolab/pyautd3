from typing import Generic, Self, TypeVar

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

M = TypeVar("M", bound=Modulation)


class RadiationPressure(Modulation, Generic[M]):
    target: M

    def __init__(self: Self, target: M) -> None:
        self.target = target

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return Base().modulation_with_radiation_pressure(self.target._modulation_ptr())
