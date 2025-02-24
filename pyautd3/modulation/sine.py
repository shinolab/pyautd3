from enum import Enum
from typing import Generic, Self, TypeVar

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.defined.angle import Angle, rad
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.utils import _validate_u8
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import SineOption as SineOption_
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

T = TypeVar("T", int, float)


class SineOption:
    intensity: int
    offset: int
    phase: Angle
    clamp: bool
    sampling_config: SamplingConfig

    def __init__(
        self: Self,
        *,
        intensity: int = 0xFF,
        offset: int = 0x80,
        phase: Angle | None = None,
        clamp: bool = False,
        sampling_config: SamplingConfig | None = None,
    ) -> None:
        self.intensity = _validate_u8(intensity)
        self.offset = _validate_u8(offset)
        self.phase = phase or 0.0 * rad
        self.clamp = clamp
        self.sampling_config = sampling_config or SamplingConfig.FREQ_4K

    def _inner(self: Self) -> SineOption_:
        return SineOption_(
            self.intensity,
            self.offset,
            self.phase._inner(),
            self.clamp,
            self.sampling_config.division,
        )


class SineMode(Enum):
    Exact = 0
    ExactFloat = 1
    Nearest = 2


class Sine(Modulation, Generic[T]):
    _mode: SineMode
    freq: Freq[T]
    option: SineOption

    def __init__(self: Self, freq: Freq[T], option: SineOption) -> None:
        super().__init__()
        match freq.hz():
            case int():
                self._mode = SineMode.Exact
            case _:
                self._mode = SineMode.ExactFloat
        self.freq = freq
        self.option = option

    def into_nearest(self: Self) -> "Sine":
        match self._mode:
            case SineMode.ExactFloat:
                new = Sine(self.freq, self.option)
                new._mode = SineMode.Nearest
                return new
            case _:
                raise TypeError

    def _modulation_ptr(self) -> ModulationPtr:
        match self._mode:
            case SineMode.Exact:
                return Base().modulation_sine_exact(self.freq.hz(), self.option._inner())  # type: ignore[arg-type]
            case SineMode.ExactFloat:
                return Base().modulation_sine_exact_float(self.freq.hz(), self.option._inner())
            case SineMode.Nearest:  # pragma: no cover
                return Base().modulation_sine_nearest(self.freq.hz(), self.option._inner())
