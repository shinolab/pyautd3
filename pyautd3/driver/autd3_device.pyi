from typing import Self
import numpy as np
from numpy.typing import ArrayLike
import pyautd3.native_methods.autd3capi_driver as consts



class AUTD3():
    TRANS_SPACING: float
    DEVICE_WIDTH: float
    DEVICE_HEIGHT: float
    NUM_TRANS_IN_X: int
    NUM_TRANS_IN_Y: int
    NUM_TRANS_IN_UNIT: int
    def __init__(self, pos: ArrayLike) -> None: ...
    def with_rotation(self, rotation: np.ndarray) -> AUTD3: ...
    @property
    def position(self) -> np.ndarray: ...
    @property
    def rotation(self) -> np.ndarray: ...
