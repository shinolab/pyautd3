from typing import TypeVar

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.angle import Angle, rad
from pyautd3.driver.defined.freq import Freq, Hz
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.utils import _validate_u8
from pyautd3.modulation.sampling_mode import ISamplingMode, SamplingModeExact, SamplingModeExactFloat, SamplingModeNearest
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

T = TypeVar("T", int, float)


class Sine(Modulation["Sine"]):
    _mode: ISamplingMode
    _intensity: int
    _offset: int
    _phase: Angle
    _clamp: bool

    def __private__init__(self: "Sine", mode: ISamplingMode) -> None:
        super().__init__(SamplingConfig(10))
        self._mode = mode
        self._intensity = 0xFF
        self._offset = 0xFF
        self._phase = 0 * rad
        self._clamp = False

    def __init__(self: "Sine", freq: Freq[T]) -> None:
        match freq.hz:
            case int():
                self.__private__init__(SamplingModeExact(freq))  # type: ignore[arg-type]
            case _:
                self.__private__init__(SamplingModeExactFloat(freq))

    @classmethod
    def nearest(cls: "type[Sine]", freq: Freq[float]) -> "Sine":
        sine = super().__new__(cls)
        sine.__private__init__(SamplingModeNearest(freq))
        return sine

    @property
    def freq(self: "Sine") -> Freq[int] | Freq[float]:
        return self._mode.sine_freq(self._modulation_ptr()) * Hz

    def with_intensity(self: "Sine", intensity: int) -> "Sine":
        self._intensity = _validate_u8(intensity)
        return self

    @property
    def intensity(self: "Sine") -> int:
        return self._intensity

    def with_offset(self: "Sine", offset: int) -> "Sine":
        self._offset = _validate_u8(offset)
        return self

    @property
    def offset(self: "Sine") -> int:
        return self._offset

    def with_phase(self: "Sine", phase: Angle) -> "Sine":
        self._phase = phase
        return self

    @property
    def phase(self: "Sine") -> Angle:
        return self._phase

    def with_clamp(self: "Sine", clamp: bool) -> "Sine":  # noqa: FBT001
        self._clamp = clamp
        return self

    @property
    def clamp(self: "Sine") -> bool:
        return self._clamp

    def _modulation_ptr(self: "Sine") -> ModulationPtr:
        return self._mode.sine_ptr(
            self._config._inner,
            self._intensity,
            self._offset,
            self._phase,
            self._clamp,
            self._loop_behavior,
        )
