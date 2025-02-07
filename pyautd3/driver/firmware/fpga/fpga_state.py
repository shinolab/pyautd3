from typing import Self

from pyautd3.native_methods.autd3 import Segment


class FPGAState:
    _state: int

    def __init__(self: Self, info: int) -> None:
        self._state = info

    def is_thermal_assert(self: Self) -> bool:
        return (self._state & (1 << 0)) != 0

    def current_mod_segment(self: Self) -> Segment:
        match int(self._state) & (1 << 1):
            case 0:
                return Segment.S0
            case _:
                return Segment.S1

    def current_stm_segment(self: Self) -> Segment | None:
        if not self.is_stm_mode():
            return None

        match int(self._state) & (1 << 2):
            case 0:
                return Segment.S0
            case _:
                return Segment.S1

    def current_gain_segment(self: Self) -> Segment | None:
        if not self.is_gain_mode():
            return None

        match int(self._state) & (1 << 2):
            case 0:
                return Segment.S0
            case _:
                return Segment.S1

    def is_gain_mode(self: Self) -> bool:
        return (int(self._state) & (1 << 3)) != 0

    def is_stm_mode(self: Self) -> bool:
        return not self.is_gain_mode()
