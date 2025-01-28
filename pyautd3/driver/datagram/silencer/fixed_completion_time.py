from typing import Self

from pyautd3.native_methods.autd3capi import FixedCompletionTime as FixedCompletionTime_
from pyautd3.utils import Duration


class FixedCompletionTime:
    intensity: Duration
    phase: Duration
    strict_mode: bool

    def __init__(self: Self, *, intensity: Duration | None = None, phase: Duration | None = None, strict_mode: bool = True) -> None:
        self.intensity = intensity or Duration.from_micros(250)
        self.phase = phase or Duration.from_micros(1000)
        self.strict_mode = strict_mode

    def _inner(self: Self) -> FixedCompletionTime_:
        return FixedCompletionTime_(self.intensity._inner, self.phase._inner, self.strict_mode)
