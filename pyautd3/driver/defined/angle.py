from typing import Self

import numpy as np

from pyautd3.native_methods.autd3 import Angle as Angle_


class Angle:
    _value: float

    def __new__(cls: type["Angle"]) -> "Angle":
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["Angle"], value: float) -> "Angle":
        ins = super().__new__(cls)
        ins._value = value
        return ins

    def radian(self: Self) -> float:
        return self._value

    def _inner(self: Self) -> Angle_:
        return Angle_(self._value)

    def __eq__(self: Self, other: object) -> bool:
        return isinstance(other, Angle) and self._value == other._value

    class _UnitRad:
        def __new__(cls: type["Angle._UnitRad"]) -> "Angle._UnitRad":
            raise NotImplementedError

        @classmethod
        def __private_new__(cls: type["Angle._UnitRad"]) -> "Angle._UnitRad":
            return super().__new__(cls)

        def __rmul__(self: Self, other: float) -> "Angle":
            return Angle.__private_new__(other)

    class _UnitDegree:
        def __new__(cls: type["Angle._UnitDegree"]) -> "Angle._UnitDegree":
            raise NotImplementedError

        @classmethod
        def __private_new__(cls: type["Angle._UnitDegree"]) -> "Angle._UnitDegree":
            return super().__new__(cls)

        def __rmul__(self: Self, other: float) -> "Angle":
            return Angle.__private_new__(np.deg2rad(other))


rad: Angle._UnitRad = Angle._UnitRad.__private_new__()
deg: Angle._UnitDegree = Angle._UnitDegree.__private_new__()
