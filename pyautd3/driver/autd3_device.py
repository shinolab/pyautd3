import numpy as np
from numpy.typing import ArrayLike

import pyautd3.native_methods.autd3capi_driver as native
from pyautd3.native_methods.utils import ConstantADT


class AUTD3(metaclass=ConstantADT):
    _pos: np.ndarray
    _rot: np.ndarray

    def __init__(self: "AUTD3", pos: ArrayLike) -> None:
        self._pos = np.array(pos)
        self._rot = np.array([1, 0, 0, 0])

    def with_rotation(self: "AUTD3", rot: ArrayLike) -> "AUTD3":
        self._rot = np.array(rot)
        return self

    TRANS_SPACING: float = native.TRANS_SPACING_MM
    DEVICE_WIDTH: float = native.DEVICE_WIDTH_MM
    DEVICE_HEIGHT: float = native.DEVICE_HEIGHT_MM
    NUM_TRANS_IN_X: int = native.NUM_TRANS_IN_X
    NUM_TRANS_IN_Y: int = native.NUM_TRANS_IN_Y
    NUM_TRANS_IN_UNIT: int = native.NUM_TRANS_IN_UNIT
