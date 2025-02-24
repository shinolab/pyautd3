from enum import Enum
from typing import Generic, Self, TypeVar

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.utils import _validate_u8
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import SquareOption as SquareOption_
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

T = TypeVar("T", int, float)


class SquareOption:
    low: int
    high: int
    duty: float
    sampling_config: SamplingConfig

    def __init__(
        self: Self,
        *,
        low: int = 0x00,
        high: int = 0xFF,
        duty: float = 0.5,
        sampling_config: SamplingConfig | None = None,
    ) -> None:
        self.low = _validate_u8(low)
        self.high = _validate_u8(high)
        self.duty = duty
        self.sampling_config = sampling_config or SamplingConfig.FREQ_4K

    def _inner(self: Self) -> SquareOption_:
        return SquareOption_(
            self.low,
            self.high,
            self.duty,
            self.sampling_config.division,
        )


class SquareMode(Enum):
    Exact = 0
    ExactFloat = 1
    Nearest = 2


class Square(Modulation, Generic[T]):
    _mode: SquareMode
    freq: Freq[T]
    option: SquareOption

    def __init__(self: Self, freq: Freq[T], option: SquareOption) -> None:
        super().__init__()
        match freq.hz():
            case int():
                self._mode = SquareMode.Exact
            case _:
                self._mode = SquareMode.ExactFloat
        self.freq = freq
        self.option = option or SquareOption()

    def into_nearest(self: Self) -> "Square":
        match self._mode:
            case SquareMode.ExactFloat:
                new = Square(self.freq, self.option)
                new._mode = SquareMode.Nearest
                return new
            case _:
                raise TypeError

    def _modulation_ptr(self) -> ModulationPtr:
        match self._mode:
            case SquareMode.Exact:
                return Base().modulation_square_exact(self.freq.hz(), self.option._inner())  # type: ignore[arg-type]
            case SquareMode.ExactFloat:
                return Base().modulation_square_exact_float(self.freq.hz(), self.option._inner())
            case SquareMode.Nearest:  # pragma: no cover
                return Base().modulation_square_nearest(self.freq.hz(), self.option._inner())
