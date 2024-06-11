from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr


class Uniform(Gain["Uniform"]):
    _intensity: EmitIntensity
    _phase: Phase

    def __init__(self: "Uniform", intensity: int | EmitIntensity) -> None:
        super().__init__()
        self._intensity = EmitIntensity(intensity)
        self._phase = Phase(0)

    @property
    def intensity(self: "Uniform") -> EmitIntensity:
        return self._intensity

    def with_phase(self: "Uniform", phase: int | Phase) -> "Uniform":
        self._phase = Phase(phase)
        return self

    @property
    def phase(self: "Uniform") -> Phase:
        return self._phase

    def _gain_ptr(self: "Uniform", _: Geometry) -> GainPtr:
        return Base().gain_uniform(self._intensity.value, self._phase.value)
