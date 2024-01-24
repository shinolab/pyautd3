from ctypes import c_double

import numpy as np

from pyautd3.native_methods.autd3capi import NativeMethods as Base


class Angle:
    """Angle."""

    _value: float

    def __new__(cls: type["Angle"]) -> "Angle":
        """DO NOT USE THIS CONSTRUCTOR."""
        raise NotImplementedError

    @classmethod
    def __private_new__(cls: type["Angle"], value: float) -> "Angle":
        ins = super().__new__(cls)
        ins._value = value
        return ins

    @staticmethod
    def new_radian(value: float) -> "Angle":
        """Create by radian."""
        return Angle.__private_new__(value)

    @staticmethod
    def new_degree(value: float) -> "Angle":
        """Create by degree."""
        return Angle.__private_new__(np.deg2rad(value))

    @property
    def radian(self: "Angle") -> float:
        """Angle in radian."""
        return self._value

    class _UnitRad:
        def __new__(cls: type["Angle._UnitRad"]) -> "Angle._UnitRad":
            """DO NOT USE THIS CONSTRUCTOR."""
            raise NotImplementedError

        @classmethod
        def __private_new__(cls: type["Angle._UnitRad"]) -> "Angle._UnitRad":
            return super().__new__(cls)

        def __rmul__(self: "Angle._UnitRad", other: float) -> "Angle":
            return Angle.new_radian(other)

    class _UnitDegree:
        def __new__(cls: type["Angle._UnitDegree"]) -> "Angle._UnitDegree":
            """DO NOT USE THIS CONSTRUCTOR."""
            raise NotImplementedError

        @classmethod
        def __private_new__(cls: type["Angle._UnitDegree"]) -> "Angle._UnitDegree":
            return super().__new__(cls)

        def __rmul__(self: "Angle._UnitDegree", other: float) -> "Angle":
            return Angle.new_degree(other)


rad: Angle._UnitRad = Angle._UnitRad.__private_new__()
deg: Angle._UnitDegree = Angle._UnitDegree.__private_new__()


class EulerAngles:
    """Euler angles."""

    def __new__(cls: type["EulerAngles"]) -> "EulerAngles":
        """DO NOT USE THIS CONSTRUCTOR."""
        raise NotImplementedError

    @staticmethod
    def from_zyz(z1: Angle, y: Angle, z2: Angle) -> np.ndarray:
        """Create from Euler ZYZ.

        Arguments:
        ---------
            z1: First rotation angle
            y: Second rotation angle
            z2: Third rotation angle
        """
        v = np.zeros([4]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().rotation_from_euler_zyz(z1.radian, y.radian, z2.radian, vp)
        return v
