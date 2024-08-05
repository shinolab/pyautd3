from typing import TypeVar

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

    def __private__init__(self: "Square", mode: ISamplingMode) -> None:
        super().__init__(SamplingConfig(10))
        self._mode = mode
        self._low = 0x00
        self._high = 0xFF
        self._duty = 0.5

    def __init__(self: "Square", freq: Freq[T]) -> None:
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
    def freq(self: "Square") -> Freq[int] | Freq[float]:
        return self._mode.square_freq(self._modulation_ptr()) * Hz

    def with_low(self: "Square", low: int) -> "Square":
        self._low = _validate_u8(low)
        return self

    @property
    def low(self: "Square") -> int:
        return self._low

    def with_high(self: "Square", high: int) -> "Square":
        self._high = _validate_u8(high)
        return self

    @property
    def high(self: "Square") -> int:
        return self._high

    def with_duty(self: "Square", duty: float) -> "Square":
        self._duty = duty
        return self

    @property
    def duty(self: "Square") -> float:
        return self._duty

    def _modulation_ptr(self: "Square") -> ModulationPtr:
        return self._mode.square_ptr(
            self._config._inner,
            self._low,
            self._high,
            self._duty,
            self._loop_behavior,
        )
