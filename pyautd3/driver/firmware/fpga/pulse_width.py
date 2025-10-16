from typing import Self

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.structs import PulseWidth as _PulseWidth
from pyautd3.native_methods.utils import _validate_pulse_width, _validate_u16


class PulseWidth:
    _inner: _PulseWidth

    @classmethod
    def __private_new__(cls: type["PulseWidth"], pulse_width: _PulseWidth) -> "PulseWidth":
        ins = super().__new__(cls)
        ins._inner = pulse_width
        return ins

    def __init__(self: Self, pulse_width: int) -> None:
        self._inner = Base().pulse_width(pulse_width)

    @staticmethod
    def from_duty(duty: float) -> "PulseWidth":
        return PulseWidth.__private_new__(_validate_pulse_width(Base().pulse_width_from_duty(duty)))

    def pulse_width(self: Self) -> int:
        return _validate_u16(Base().pulse_width_pulse_width(self._inner))

    def __eq__(self: Self, other: object) -> bool:
        return isinstance(other, PulseWidth) and self.pulse_width() == other.pulse_width()

    def __hash__(self: Self) -> int:
        return self.pulse_width().__hash__()  # pragma: no cover
