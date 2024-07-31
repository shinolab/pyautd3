from .emit_intensity import EmitIntensity
from .phase import Phase


class Drive:
    _phase: Phase
    _intensity: EmitIntensity

    def __init__(self: "Drive", value: "Drive | EmitIntensity | Phase | tuple") -> None:
        if isinstance(value, tuple):
            if len(value) != 2:  # noqa: PLR2004
                raise TypeError
            if isinstance(value[0], EmitIntensity) and isinstance(value[1], Phase):
                self._intensity = value[0]
                self._phase = value[1]
            elif isinstance(value[0], Phase) and isinstance(value[1], EmitIntensity):
                self._intensity = value[1]
                self._phase = value[0]
            else:
                raise TypeError
        elif isinstance(value, Drive):
            self._phase = value.phase
            self._intensity = value.intensity
        elif isinstance(value, EmitIntensity):
            self._phase = Phase(0)
            self._intensity = value
        elif isinstance(value, Phase):
            self._phase = value
            self._intensity = EmitIntensity(0xFF)
        else:
            raise TypeError

    @property
    def phase(self: "Drive") -> Phase:
        return self._phase

    @property
    def intensity(self: "Drive") -> EmitIntensity:
        return self._intensity

    @staticmethod
    def null() -> "Drive":
        return Drive((Phase(0), EmitIntensity.minimum()))
