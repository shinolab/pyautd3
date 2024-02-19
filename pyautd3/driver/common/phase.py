from ctypes import c_uint8

from pyautd3.native_methods.autd3capi_def import NativeMethods as Def


class Phase:
    """Ultrasound phase."""

    _value: c_uint8

    def __init__(self: "Phase", phase: int) -> None:
        self._value = c_uint8(phase)

    @staticmethod
    def from_rad(value: float) -> "Phase":
        """Create by radian."""
        return Phase(int(Def().phase_from_rad(value)))

    @property
    def value(self: "Phase") -> int:
        """Phase."""
        return self._value.value

    @property
    def radian(self: "Phase") -> float:
        """Radian."""
        return float(Def().phase_to_rad(self.value))

    class _UnitRad:
        def __new__(cls: type["Phase._UnitRad"]) -> "Phase._UnitRad":
            """DO NOT USE THIS CONSTRUCTOR."""
            raise NotImplementedError

        @classmethod
        def __private_new__(cls: type["Phase._UnitRad"]) -> "Phase._UnitRad":
            return super().__new__(cls)

        def __rmul__(self: "Phase._UnitRad", other: float) -> "Phase":
            return Phase.from_rad(other)

    def __eq__(self: "Phase", __value: object) -> bool:
        return isinstance(__value, Phase) and self.value == __value.value

    def __str__(self: "Phase") -> str:
        return f"Phase({self.value})"

    def __repr__(self: "Phase") -> str:
        return f"Phase({self.value})"


rad: Phase._UnitRad = Phase._UnitRad.__private_new__()
