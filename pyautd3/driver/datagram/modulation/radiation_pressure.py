from typing import Generic, TypeVar

from pyautd3.driver.datagram.modulation.modulation import IModulation
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import ModulationPtr

from .cache import IModulationWithCache

M = TypeVar("M", bound=IModulation)


class RadiationPressure(IModulationWithCache, IModulation, Generic[M]):
    """Modulation for modulating radiation pressure."""

    _m: M

    def __init__(self: "RadiationPressure", m: M) -> None:
        self._m = m

    def _modulation_ptr(self: "RadiationPressure[M]") -> ModulationPtr:
        return Base().modulation_with_radiation_pressure(self._m._modulation_ptr())


class IModulationWithRadiationPressure:
    """Modulation interface of RadiationPressure."""

    def with_radiation_pressure(self: M) -> "RadiationPressure[M]":
        """Apply modulation to radiation pressure instead of amplitude."""
        return RadiationPressure(self)
