from typing import Self

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.native_methods.autd3capi_driver import (
    DEVICE_HEIGHT_MM,
    DEVICE_WIDTH_MM,
    NUM_TRANS_IN_UNIT,
    NUM_TRANS_IN_X,
    NUM_TRANS_IN_Y,
    TRANS_SPACING_MM,
)
from pyautd3.native_methods.utils import ConstantADT


class AUTD3(metaclass=ConstantADT):
    _pos: np.ndarray
    _rot: np.ndarray

    def __init__(self: Self, pos: ArrayLike) -> None:
        self._pos = np.array(pos)
        self._rot = np.array([1, 0, 0, 0])

    def with_rotation(self: Self, rot: ArrayLike) -> Self:
        self._rot = np.array(rot)
        return self

    TRANS_SPACING: float = TRANS_SPACING_MM
    DEVICE_WIDTH: float = DEVICE_WIDTH_MM
    DEVICE_HEIGHT: float = DEVICE_HEIGHT_MM
    NUM_TRANS_IN_X: int = NUM_TRANS_IN_X
    NUM_TRANS_IN_Y: int = NUM_TRANS_IN_Y
    NUM_TRANS_IN_UNIT: int = NUM_TRANS_IN_UNIT
