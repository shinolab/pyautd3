from typing import Self

from .emit_intensity import EmitIntensity
from .phase import Phase


class Drive:
    phase: Phase
    intensity: EmitIntensity

    def __init__(self: Self, *, intensity: EmitIntensity, phase: Phase) -> None:
        self.phase = phase
        self.intensity = intensity

    NULL: "Drive" = None  # type: ignore[assignment]


Drive.NULL = Drive(phase=Phase.ZERO, intensity=EmitIntensity.MIN)
