from typing import Self

from pyautd3.driver.utils import _validate_nonzero_u16
from pyautd3.native_methods.autd3capi import FixedCompletionSteps as FixedCompletionSteps_


class FixedCompletionSteps:
    intensity: int
    phase: int
    strict: bool

    def __init__(self: Self, *, intensity: int = 10, phase: int = 40, strict: bool = True) -> None:
        self.intensity = _validate_nonzero_u16(intensity)
        self.phase = _validate_nonzero_u16(phase)
        self.strict = strict

    def _inner(self: Self) -> FixedCompletionSteps_:
        return FixedCompletionSteps_(self.intensity, self.phase, self.strict)
