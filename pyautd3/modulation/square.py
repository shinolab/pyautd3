from typing import TypeVar

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.geometry.geometry import Geometry
from pyautd3.modulation.sampling_mode import ISamplingMode, SamplingModeExact, SamplingModeExactFloat, SamplingModeNearest
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

T = TypeVar("T", int, float)


class Square(Modulation["Square"]):
    _mode: ISamplingMode
    _low: EmitIntensity
    _high: EmitIntensity
    _duty: float

    def __private__init__(self: "Square", mode: ISamplingMode) -> None:
        super().__init__(SamplingConfig.Division(5120))
        self._mode = mode
        self._low = EmitIntensity.minimum()
        self._high = EmitIntensity.maximum()
        self._duty = 0.5

    def __init__(self: "Square", freq: Freq[T]) -> None:
        match freq.hz:
            case int():
                self.__private__init__(SamplingModeExact(freq))  # type: ignore[arg-type]
            case _:
                self.__private__init__(SamplingModeExactFloat(freq))

    @classmethod
    def with_freq_nearest(cls: "type[Square]", freq: Freq[float]) -> "Square":
        sine = super().__new__(cls)
        sine.__private__init__(SamplingModeNearest(freq))
        return sine

    def with_low(self: "Square", low: int | EmitIntensity) -> "Square":
        self._low = EmitIntensity(low)
        return self

    @property
    def low(self: "Square") -> EmitIntensity:
        return self._low

    def with_high(self: "Square", high: int | EmitIntensity) -> "Square":
        self._high = EmitIntensity(high)
        return self

    @property
    def high(self: "Square") -> EmitIntensity:
        return self._high

    def with_duty(self: "Square", duty: float) -> "Square":
        self._duty = duty
        return self

    @property
    def duty(self: "Square") -> float:
        return self._duty

    def _modulation_ptr(self: "Square", _: Geometry) -> ModulationPtr:
        return self._mode.square_ptr(
            self._config,
            self._low,
            self._high,
            self._duty,
            self._loop_behavior,
        )
