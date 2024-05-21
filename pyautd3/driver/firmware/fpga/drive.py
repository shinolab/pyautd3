from .emit_intensity import EmitIntensity
from .phase import Phase


class Drive:
    _phase: Phase
    _intensity: EmitIntensity

    def __init__(self: "Drive", phase: Phase, intensity: EmitIntensity) -> None:
        self._phase = phase
        self._intensity = intensity

    @property
    def phase(self: "Drive") -> Phase:
        return self._phase

    @property
    def intensity(self: "Drive") -> EmitIntensity:
        return self._intensity

    @staticmethod
    def null() -> "Drive":
        return Drive(Phase(0), EmitIntensity.minimum())
