from typing import Self

from pyautd3.driver.utils import _validate_u8
from pyautd3.native_methods.autd3 import Intensity as Intensity_


class Intensity:
    value: int

    def __init__(self: Self, intensity: int) -> None:
        self.value = _validate_u8(intensity)

    def __floordiv__(self: Self, other: int) -> "Intensity":
        return Intensity(self.value // other)

    def __eq__(self: Self, __value: object, /) -> bool:
        return isinstance(__value, Intensity) and self.value == __value.value

    def __hash__(self: Self) -> int:
        return self.value.__hash__()  # pragma: no cover

    def __str__(self: Self) -> str:
        return f"Intensity({self.value})"

    def __repr__(self: Self) -> str:
        return f"Intensity({self.value})"

    def _inner(self: Self) -> Intensity_:
        return Intensity_(self.value)

    MIN: "Intensity" = None  # type: ignore[assignment]
    MAX: "Intensity" = None  # type: ignore[assignment]


Intensity.MIN = Intensity(0x00)
Intensity.MAX = Intensity(0xFF)
