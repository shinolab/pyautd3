from pyautd3.driver.firmware.fpga import EmitIntensity
from pyautd3.native_methods.autd3capi_gain_holo import EmissionConstraintWrap
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo
from pyautd3.native_methods.utils import ConstantADT

__all__ = ["EmissionConstraint"]


class EmissionConstraint(metaclass=ConstantADT):
    def __new__(cls: type["EmissionConstraint"]) -> "EmissionConstraint":
        raise NotImplementedError

    Normalize: EmissionConstraintWrap = GainHolo().gain_holo_constraint_normalize()

    @staticmethod
    def Uniform(value: int | EmitIntensity) -> EmissionConstraintWrap:  # noqa: N802
        return GainHolo().gain_holo_constraint_uniform(EmitIntensity(value).value)

    @staticmethod
    def Clamp(min_v: int | EmitIntensity, max_v: int | EmitIntensity) -> EmissionConstraintWrap:  # noqa: N802
        return GainHolo().gain_holo_constraint_clamp(EmitIntensity(min_v).value, EmitIntensity(max_v).value)

    @staticmethod
    def Multiply(value: float) -> EmissionConstraintWrap:  # noqa: N802
        return GainHolo().gain_holo_constraint_multiply(value)
