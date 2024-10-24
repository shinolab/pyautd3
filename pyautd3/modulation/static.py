from typing import Self

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.fir import IntoModulationFir
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.utils import _validate_u8
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr


class Static(
    IntoModulationCache["Static"],
    IntoModulationFir["Static"],
    IntoModulationRadiationPressure["Static"],
    ModulationBase["Static"],
):
    _intensity: int

    def __init__(self: Self, intensity: int | None = None) -> None:
        super().__init__()
        match intensity:
            case None:
                self._intensity = 0xFF
            case int():
                self._intensity = _validate_u8(intensity)
            case _:
                raise TypeError

    @staticmethod
    def with_intensity(intensity: int) -> "Static":
        return Static(intensity)

    @property
    def intensity(self: Self) -> int:
        return self._intensity

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return Base().modulation_static(self._intensity, self._loop_behavior)
