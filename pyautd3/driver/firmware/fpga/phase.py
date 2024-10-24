from typing import Self

from pyautd3.driver.defined import Angle
from pyautd3.native_methods.autd3capi import NativeMethods as Base


class Phase:
    _value: int

    def __init__(self: Self, phase: "int | Angle | Phase") -> None:
        match phase:
            case int():
                self._value = phase
            case Angle():
                self._value = int(Base().phase_from_rad(phase.radian))
            case Phase():
                self._value = phase._value
            case _:
                raise TypeError

    @property
    def value(self: Self) -> int:
        return int(self._value)

    @property
    def radian(self: Self) -> float:
        return float(Base().phase_to_rad(self.value))

    def __eq__(self: Self, other: object) -> bool:
        return isinstance(other, Phase) and self.value == other.value

    def __str__(self: Self) -> str:
        return f"Phase({self.value})"

    def __repr__(self: Self) -> str:
        return f"Phase({self.value})"
