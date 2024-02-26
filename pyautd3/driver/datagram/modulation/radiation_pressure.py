from typing import Generic, TypeVar

from pyautd3.driver.datagram.modulation.modulation import ModulationBase
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import ModulationPtr

from .cache import IntoModulationCache

M = TypeVar("M", bound=ModulationBase)


class RadiationPressure(
    IntoModulationCache["RadiationPressure[M]"],
    ModulationBase["RadiationPressure[M]"],
    Generic[M],
):
    """Modulation for modulating radiation pressure."""

    _m: M

    def __init__(self: "RadiationPressure", m: M) -> None:
        self._m = m
        self._loop_behavior = m._loop_behavior

    def _modulation_ptr(self: "RadiationPressure[M]") -> ModulationPtr:
        return Base().modulation_with_radiation_pressure(self._m._modulation_ptr(), self._loop_behavior._internal)


class IntoModulationRadiationPressure(ModulationBase[M], Generic[M]):
    """Modulation interface of RadiationPressure."""

    def with_radiation_pressure(self: M) -> "RadiationPressure[M]":
        """Apply modulation to radiation pressure instead of amplitude."""
        return RadiationPressure(self)
