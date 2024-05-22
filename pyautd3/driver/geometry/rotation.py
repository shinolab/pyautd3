from ctypes import c_double

import numpy as np

from pyautd3.driver.defined.angle import Angle
from pyautd3.native_methods.autd3capi import NativeMethods as Base


class EulerAngles:
    def __new__(cls: type["EulerAngles"]) -> "EulerAngles":
        raise NotImplementedError

    @staticmethod
    def ZYZ(z1: Angle, y: Angle, z2: Angle) -> np.ndarray:  # noqa: N802
        v = np.zeros([4]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().rotation_from_euler_zyz(z1.radian, y.radian, z2.radian, vp)
        return v
