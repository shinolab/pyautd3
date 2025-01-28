from typing import Self

from .emit_intensity import EmitIntensity
from .phase import Phase


class Drive:
    phase: Phase
    intensity: EmitIntensity

    def __init__(self: Self, *, intensity: EmitIntensity, phase: Phase) -> None:
        self.phase = phase
        self.intensity = intensity

    @staticmethod
    def NULL() -> "Drive":  # noqa: N802
        return Drive(phase=Phase(0), intensity=EmitIntensity.minimum())
