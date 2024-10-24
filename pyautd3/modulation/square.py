from typing import Self, TypeVar

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq, Hz
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.utils import _validate_u8
from pyautd3.modulation.sampling_mode import ISamplingMode, SamplingModeExact, SamplingModeExactFloat, SamplingModeNearest
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

T = TypeVar("T", int, float)


class Square(Modulation["Square"]):
    _mode: ISamplingMode
    _low: int
    _high: int
    _duty: float

    def __private__init__(self: Self, mode: ISamplingMode) -> None:
        super().__init__(SamplingConfig(10))
        self._mode = mode
        self._low = 0x00
        self._high = 0xFF
        self._duty = 0.5

    def __init__(self: Self, freq: Freq[T]) -> None:
        match freq.hz:
            case int():
                self.__private__init__(SamplingModeExact(freq))  # type: ignore[arg-type]
            case _:
                self.__private__init__(SamplingModeExactFloat(freq))

    @classmethod
    def nearest(cls: "type[Square]", freq: Freq[float]) -> "Square":
        sine = super().__new__(cls)
        sine.__private__init__(SamplingModeNearest(freq))
        return sine

    @property
    def freq(self: Self) -> Freq[int] | Freq[float]:
        return self._mode.square_freq() * Hz

    def with_low(self: Self, low: int) -> Self:
        self._low = _validate_u8(low)
        return self

    @property
    def low(self: Self) -> int:
        return self._low

    def with_high(self: Self, high: int) -> Self:
        self._high = _validate_u8(high)
        return self

    @property
    def high(self: Self) -> int:
        return self._high

    def with_duty(self: Self, duty: float) -> Self:
        self._duty = duty
        return self

    @property
    def duty(self: Self) -> float:
        return self._duty

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return self._mode.square_ptr(
            self._config._inner,
            self._low,
            self._high,
            self._duty,
            self._loop_behavior,
        )
