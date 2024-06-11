from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.datagram.modulation.transform import IntoModulationTransform
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.geometry.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr


class Static(
    IntoModulationCache["Static"],
    IntoModulationRadiationPressure["Static"],
    IntoModulationTransform["Static"],
    ModulationBase["Static"],
):
    _intensity: EmitIntensity

    def __init__(self: "Static", intensity: int | EmitIntensity | None = None) -> None:
        super().__init__()
        self._intensity = EmitIntensity.maximum() if intensity is None else EmitIntensity(intensity)

    @staticmethod
    def with_intensity(intensity: int | EmitIntensity) -> "Static":
        return Static(intensity)

    @property
    def intensity(self: "Static") -> EmitIntensity:
        return self._intensity

    def _modulation_ptr(self: "Static", _: Geometry) -> ModulationPtr:
        return Base().modulation_static(self._intensity.value, self._loop_behavior)
