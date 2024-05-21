from ctypes import c_uint8

from pyautd3.driver.defined import Angle
from pyautd3.native_methods.autd3capi import NativeMethods as Base


class Phase:
    _value: c_uint8

    def __init__(self: "Phase", phase: int | Angle) -> None:
        match phase:
            case int():
                self._value = c_uint8(phase)
            case _:
                self._value = c_uint8(Base().phase_from_rad(phase.radian))  # type: ignore[arg-type]

    @property
    def value(self: "Phase") -> int:
        return int(self._value.value)

    @property
    def radian(self: "Phase") -> float:
        return float(Base().phase_to_rad(self.value))

    def __eq__(self: "Phase", other: object) -> bool:
        return isinstance(other, Phase) and self.value == other.value

    def __str__(self: "Phase") -> str:
        return f"Phase({self.value})"

    def __repr__(self: "Phase") -> str:
        return f"Phase({self.value})"
