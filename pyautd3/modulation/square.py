from typing import Self, TypeVar

from pyautd3.derive import builder, datagram, modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import ModulationWithSamplingConfig
from pyautd3.driver.defined.freq import Freq, Hz
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.modulation.sampling_mode import ISamplingMode, SamplingModeExact, SamplingModeExactFloat, SamplingModeNearest
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

T = TypeVar("T", int, float)


@modulation
@datagram
@datagram_with_segment
@builder
class Square(ModulationWithSamplingConfig):
    _mode: ISamplingMode
    _param_low_u8: int
    _param_high_u8: int
    _param_duty: float

    def __private__init__(self: Self, mode: ISamplingMode) -> None:
        super().__init__(SamplingConfig(10))
        self._mode = mode
        self._param_low_u8 = 0x00
        self._param_high_u8 = 0xFF
        self._param_duty = 0.5

    def __init__(self: Self, freq: Freq[T]) -> None:
        match freq.hz:
            case int():
                self.__private__init__(SamplingModeExact(freq))  # type: ignore[arg-type]
            case _:
                self.__private__init__(SamplingModeExactFloat(freq))

    @classmethod
    def nearest(cls: "type[Square]", freq: Freq[float]) -> "Square":
        ins = super().__new__(cls)
        ins.__private__init__(SamplingModeNearest(freq))
        return ins

    @property
    def freq(self: Self) -> Freq[int] | Freq[float]:
        return self._mode.square_freq() * Hz

    def _modulation_ptr(self) -> ModulationPtr:
        return self._mode.square_ptr(
            self._config._inner,
            self._param_low_u8,
            self._param_high_u8,
            self._param_duty,
            self._loop_behavior,
        )
