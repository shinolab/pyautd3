from typing import Generic, Self, TypeVar

from pyautd3.derive import datagram, modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

M = TypeVar("M", bound=Modulation)


@datagram
@datagram_with_segment
@modulation
class RadiationPressure(Modulation, Generic[M]):
    _m: M

    def __init__(self: Self, m: M) -> None:
        self._m = m
        self._loop_behavior = m._loop_behavior

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return Base().modulation_with_radiation_pressure(self._m._modulation_ptr(), self._loop_behavior)
