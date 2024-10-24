from typing import Generic, Self, TypeVar

from pyautd3.driver.datagram.modulation.modulation import ModulationBase
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

from .cache import IntoModulationCache

M = TypeVar("M", bound=ModulationBase)


class RadiationPressure(
    IntoModulationCache["RadiationPressure[M]"],
    ModulationBase["RadiationPressure[M]"],
    Generic[M],
):
    _m: M

    def __init__(self: Self, m: M) -> None:
        self._m = m
        self._loop_behavior = m._loop_behavior

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return Base().modulation_with_radiation_pressure(self._m._modulation_ptr(), self._loop_behavior)


class IntoModulationRadiationPressure(ModulationBase[M], Generic[M]):
    def with_radiation_pressure(self: M) -> RadiationPressure[M]:
        return RadiationPressure(self)
