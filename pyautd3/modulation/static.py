from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.datagram.modulation.transform import IntoModulationTransform
from pyautd3.driver.utils import _validate_u8
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr


class Static(
    IntoModulationCache["Static"],
    IntoModulationRadiationPressure["Static"],
    IntoModulationTransform["Static"],
    ModulationBase["Static"],
):
    _intensity: int

    def __init__(self: "Static", intensity: int | None = None) -> None:
        if isinstance(intensity, float):
            raise TypeError
        super().__init__()
        self._intensity = 0xFF if intensity is None else _validate_u8(intensity)

    @staticmethod
    def with_intensity(intensity: int) -> "Static":
        return Static(intensity)

    @property
    def intensity(self: "Static") -> int:
        return self._intensity

    def _modulation_ptr(self: "Static") -> ModulationPtr:
        return Base().modulation_static(self._intensity, self._loop_behavior)
