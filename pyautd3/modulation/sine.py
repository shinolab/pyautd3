from typing import TypeVar

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.angle import Angle, rad
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.geometry import Geometry
from pyautd3.modulation.sampling_mode import ISamplingMode, SamplingModeExact, SamplingModeExactFloat, SamplingModeNearest
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

T = TypeVar("T", int, float)


class Sine(Modulation["Sine"]):
    _mode: ISamplingMode
    _intensity: EmitIntensity
    _offset: EmitIntensity
    _phase: Angle

    def __private__init__(self: "Sine", mode: ISamplingMode) -> None:
        super().__init__(SamplingConfig.Division(5120))
        self._mode = mode
        self._intensity = EmitIntensity.maximum()
        self._offset = EmitIntensity.maximum() // 2
        self._phase = 0 * rad

    def __init__(self: "Sine", freq: Freq[T]) -> None:
        match freq.hz:
            case int():
                self.__private__init__(SamplingModeExact(freq))  # type: ignore[arg-type]
            case _:
                self.__private__init__(SamplingModeExactFloat(freq))

    @classmethod
    def with_freq_nearest(cls: "type[Sine]", freq: Freq[float]) -> "Sine":
        sine = super().__new__(cls)
        sine.__private__init__(SamplingModeNearest(freq))
        return sine

    def with_intensity(self: "Sine", intensity: EmitIntensity) -> "Sine":
        self._intensity = intensity
        return self

    @property
    def intensity(self: "Sine") -> EmitIntensity:
        return self._intensity

    def with_offset(self: "Sine", offset: EmitIntensity) -> "Sine":
        self._offset = offset
        return self

    @property
    def offset(self: "Sine") -> EmitIntensity:
        return self._offset

    def with_phase(self: "Sine", phase: Angle) -> "Sine":
        self._phase = phase
        return self

    @property
    def phase(self: "Sine") -> Angle:
        return self._phase

    def _modulation_ptr(self: "Sine", _: Geometry) -> ModulationPtr:
        return self._mode.sine_ptr(
            self._config,
            self._intensity,
            self._offset,
            self._phase,
            self._loop_behavior,
        )
