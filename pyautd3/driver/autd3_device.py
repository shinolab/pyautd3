from typing import Self

import numpy as np
from numpy.typing import ArrayLike

import pyautd3.native_methods.autd3capi_driver as consts


class AUTD3:
    pos: np.ndarray
    rot: np.ndarray

    def __init__(self: Self, pos: ArrayLike, rot: ArrayLike) -> None:
        self.pos = np.array(pos)
        self.rot = np.array(rot)

    TRANS_SPACING: float = consts.TRANS_SPACING_MM
    DEVICE_WIDTH: float = consts.DEVICE_WIDTH_MM
    DEVICE_HEIGHT: float = consts.DEVICE_HEIGHT_MM
    NUM_TRANS_IN_X: int = consts.NUM_TRANS_IN_X
    NUM_TRANS_IN_Y: int = consts.NUM_TRANS_IN_Y
    NUM_TRANS_IN_UNIT: int = consts.NUM_TRANS_IN_UNIT
