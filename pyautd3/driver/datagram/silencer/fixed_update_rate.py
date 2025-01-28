from typing import Self

from pyautd3.driver.utils import _validate_nonzero_u16
from pyautd3.native_methods.autd3capi import FixedUpdateRate as FixedUpdateRate_


class FixedUpdateRate:
    intensity: int
    phase: int

    def __init__(self: Self, *, intensity: int, phase: int) -> None:
        self.intensity = _validate_nonzero_u16(intensity)
        self.phase = _validate_nonzero_u16(phase)

    def _inner(self: Self) -> FixedUpdateRate_:
        return FixedUpdateRate_(self.intensity, self.phase)
