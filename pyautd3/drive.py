from .emit_intensity import EmitIntensity
from .phase import Phase


class Drive:
    """Phase and intensity."""

    _phase: Phase
    _intensity: EmitIntensity

    def __init__(self: "Drive", phase: Phase, intensity: int | EmitIntensity) -> None:
        self._phase = phase
        self._intensity = EmitIntensity._cast(intensity)

    @property
    def phase(self: "Drive") -> Phase:
        """Phase."""
        return self._phase

    @property
    def intensity(self: "Drive") -> EmitIntensity:
        """Emission intensity."""
        return self._intensity
