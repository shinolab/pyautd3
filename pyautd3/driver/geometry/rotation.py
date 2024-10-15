import numpy as np

from pyautd3.driver.defined.angle import Angle
from pyautd3.native_methods.autd3capi import NativeMethods as Base


class EulerAngles:
    def __new__(cls: type["EulerAngles"]) -> "EulerAngles":
        raise NotImplementedError

    @staticmethod
    def XYZ(x: Angle, y: Angle, z: Angle) -> np.ndarray:  # noqa: N802
        return Base().rotation_from_euler_xyz(x.radian, y.radian, z.radian).ndarray()

    @staticmethod
    def ZYZ(z1: Angle, y: Angle, z2: Angle) -> np.ndarray:  # noqa: N802
        return Base().rotation_from_euler_zyz(z1.radian, y.radian, z2.radian).ndarray()
