from abc import ABCMeta, abstractmethod

from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.native_methods.autd3capi_gain_holo import EmissionConstraintPtr
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo

__all__ = ["EmissionConstraint"]


class IEmissionConstraint(metaclass=ABCMeta):
    @abstractmethod
    def _constraint_ptr(self: "IEmissionConstraint") -> EmissionConstraintPtr:
        pass

    def __eq__(self: "IEmissionConstraint", __value: object) -> bool:
        if not isinstance(__value, IEmissionConstraint):
            return False
        return bool(GainHolo().gain_holo_constraint_eq(self._constraint_ptr(), __value._constraint_ptr()))


class EmissionConstraint:
    """Amplitude constraint."""

    def __new__(cls: type["EmissionConstraint"]) -> "EmissionConstraint":
        """DO NOT USE THIS CONSTRUCTOR."""
        raise NotImplementedError

    class DontCare(IEmissionConstraint):
        """Do nothing (this is equivalent to `clamp(0, 1)`)."""

        def _constraint_ptr(self: "EmissionConstraint.DontCare") -> EmissionConstraintPtr:
            return GainHolo().gain_holo_constraint_dot_care()

    class Normalize(IEmissionConstraint):
        """Normalize the value by dividing the maximum value."""

        def _constraint_ptr(self: "EmissionConstraint.Normalize") -> EmissionConstraintPtr:
            return GainHolo().gain_holo_constraint_normalize()

    class Uniform(IEmissionConstraint):
        """Set all amplitudes to the specified value."""

        _value: EmitIntensity

        def __init__(self: "EmissionConstraint.Uniform", value: int | EmitIntensity) -> None:
            """Set all amplitudes to the specified value.

            Arguments:
            ---------
                value: emission intensity

            """
            self._value = EmitIntensity._cast(value)

        def _constraint_ptr(self: "EmissionConstraint.Uniform") -> EmissionConstraintPtr:
            return GainHolo().gain_holo_constraint_uniform(self._value.value)

    class Clamp(IEmissionConstraint):
        """Clamp all amplitudes to the specified range."""

        _min_v: EmitIntensity
        _max_v: EmitIntensity

        def __init__(self: "EmissionConstraint.Clamp", min_v: int | EmitIntensity, max_v: int | EmitIntensity) -> None:
            """Clamp all amplitudes to the specified range.

            Arguments:
            ---------
                min_v: minimum emission intensity
                max_v: maximum emission intensity

            """
            self._min_v = EmitIntensity._cast(min_v)
            self._max_v = EmitIntensity._cast(max_v)

        def _constraint_ptr(self: "EmissionConstraint.Clamp") -> EmissionConstraintPtr:
            return GainHolo().gain_holo_constraint_clamp(self._min_v.value, self._max_v.value)
