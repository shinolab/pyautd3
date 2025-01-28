from typing import Self

from pyautd3.driver.utils import _validate_u8
from pyautd3.native_methods.autd3 import EmitIntensity as EmitIntensity_


class EmitIntensity:
    value: int

    def __init__(self: Self, intensity: int) -> None:
        self.value = _validate_u8(intensity)

    @staticmethod
    def maximum() -> "EmitIntensity":
        return EmitIntensity(0xFF)

    @staticmethod
    def minimum() -> "EmitIntensity":
        return EmitIntensity(0x00)

    def __floordiv__(self: Self, other: int) -> "EmitIntensity":
        return EmitIntensity(self.value // other)

    def __eq__(self: Self, __value: object, /) -> bool:
        return isinstance(__value, EmitIntensity) and self.value == __value.value

    def __str__(self: Self) -> str:
        return f"EmitIntensity({self.value})"

    def __repr__(self: Self) -> str:
        return f"EmitIntensity({self.value})"

    def _inner(self: Self) -> EmitIntensity_:
        return EmitIntensity_(self.value)
