from typing import Self

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.utils import _validate_u16


class PulseWidth:
    _pulse_width: int

    @classmethod
    def __private_new__(cls: type["PulseWidth"], pulse_width: int) -> "PulseWidth":
        ins = super().__new__(cls)
        ins._pulse_width = pulse_width
        return ins

    def __init__(self: Self, pulse_width: int) -> None:
        self._pulse_width = _validate_u16(Base().pulse_width_512(pulse_width))

    @staticmethod
    def from_duty(duty: float) -> "PulseWidth":
        return PulseWidth.__private_new__(_validate_u16(Base().pulse_width_512_from_duty(duty)))

    @property
    def pulse_width(self: Self) -> int:
        return self._pulse_width
