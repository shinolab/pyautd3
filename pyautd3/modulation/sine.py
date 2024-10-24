from typing import Self, TypeVar

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

    def __private__init__(self: Self, mode: ISamplingMode) -> None:
        super().__init__(SamplingConfig(10))
        self._mode = mode
        self._intensity = 0xFF
        self._offset = 0x80
        self._phase = 0 * rad
        self._clamp = False

    def __init__(self: Self, freq: Freq[T]) -> None:
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
    def freq(self: Self) -> Freq[int] | Freq[float]:
        return self._mode.sine_freq() * Hz

    def with_intensity(self: Self, intensity: int) -> Self:
        self._intensity = _validate_u8(intensity)
        return self

    @property
    def intensity(self: Self) -> int:
        return self._intensity

    def with_offset(self: Self, offset: int) -> Self:
        self._offset = _validate_u8(offset)
        return self

    @property
    def offset(self: Self) -> int:
        return self._offset

    def with_phase(self: Self, phase: Angle) -> Self:
        self._phase = phase
        return self

    @property
    def phase(self: Self) -> Angle:
        return self._phase

    def with_clamp(self: Self, clamp: bool) -> Self:  # noqa: FBT001
        self._clamp = clamp
        return self

    @property
    def clamp(self: Self) -> bool:
        return self._clamp

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return self._mode.sine_ptr(
            self._config._inner,
            self._intensity,
            self._offset,
            self._phase,
            self._clamp,
            self._loop_behavior,
        )
