from typing import Self

from .emit_intensity import Intensity
from .phase import Phase


class Drive:
    phase: Phase
    intensity: Intensity

    def __init__(self: Self, *, intensity: Intensity, phase: Phase) -> None:
        self.phase = phase
        self.intensity = intensity

    NULL: "Drive" = None  # type: ignore[assignment]


Drive.NULL = Drive(phase=Phase.ZERO, intensity=Intensity.MIN)
