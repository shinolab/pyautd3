from typing import Self

from pyautd3.driver.defined import Angle
from pyautd3.native_methods.autd3 import Phase as Phase_
from pyautd3.native_methods.autd3capi import NativeMethods as Base


class Phase:
    value: int

    def __init__(self: Self, phase: "int | Angle") -> None:
        match phase:
            case int():
                self.value = phase
            case Angle():
                self.value = int(Base().phase_from_rad(phase.radian()))
            case _:
                raise TypeError

    def radian(self: Self) -> float:
        return float(Base().phase_to_rad(self._inner()))

    def __eq__(self: Self, other: object) -> bool:
        return isinstance(other, Phase) and self.value == other.value

    def __str__(self: Self) -> str:
        return f"Phase({self.value})"

    def __repr__(self: Self) -> str:
        return f"Phase({self.value})"

    def _inner(self: Self) -> Phase_:
        return Phase_(self.value)

    ZERO: "Phase" = None  # type: ignore[assignment]
    PI: "Phase" = None  # type: ignore[assignment]


Phase.ZERO = Phase(0x00)
Phase.PI = Phase(0x80)
