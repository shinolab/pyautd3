from typing import Self

from pyautd3.driver.utils import _validate_u8


class EmitIntensity:
    _value: int

    def __init__(self: Self, intensity: "int | EmitIntensity") -> None:
        match intensity:
            case EmitIntensity():
                self._value = intensity._value
            case int():
                self._value = _validate_u8(intensity)
            case _:
                raise TypeError

    @property
    def value(self: Self) -> int:
        return self._value

    @staticmethod
    def maximum() -> "EmitIntensity":
        return EmitIntensity(0xFF)

    @staticmethod
    def minimum() -> "EmitIntensity":
        return EmitIntensity(0x00)

    def __floordiv__(self: Self, other: int) -> "EmitIntensity":
        return EmitIntensity(self.value // other)

    def __eq__(self: Self, __value: object) -> bool:
        return isinstance(__value, EmitIntensity) and self.value == __value.value

    def __str__(self: Self) -> str:
        return f"EmitIntensity({self.value})"

    def __repr__(self: Self) -> str:
        return f"EmitIntensity({self.value})"
