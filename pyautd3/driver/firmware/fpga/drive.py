from typing import Self

from .emit_intensity import EmitIntensity
from .phase import Phase


class Drive:
    _phase: Phase
    _intensity: EmitIntensity

    def __init__(self: Self, value: "Drive | EmitIntensity | Phase | tuple") -> None:
        match value:
            case tuple():
                if len(value) != 2:  # noqa: PLR2004
                    raise TypeError
                match value[0], value[1]:
                    case EmitIntensity(), Phase():
                        self._intensity = value[0]
                        self._phase = value[1]
                    case Phase(), EmitIntensity():
                        self._intensity = value[1]
                        self._phase = value[0]
                    case _:
                        raise TypeError
            case Drive():
                self._phase = value.phase
                self._intensity = value.intensity
            case EmitIntensity():
                self._phase = Phase(0)
                self._intensity = value
            case Phase():
                self._phase = value
                self._intensity = EmitIntensity(0xFF)
            case _:
                raise TypeError

    @property
    def phase(self: Self) -> Phase:
        return self._phase

    @property
    def intensity(self: Self) -> EmitIntensity:
        return self._intensity

    @staticmethod
    def NULL() -> "Drive":  # noqa: N802
        return Drive((Phase(0), EmitIntensity.minimum()))
