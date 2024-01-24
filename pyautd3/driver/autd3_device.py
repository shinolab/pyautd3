import numpy as np
from numpy.typing import ArrayLike

from pyautd3.native_methods.autd3capi_def import (
    DEVICE_HEIGHT_MM,
    DEVICE_WIDTH_MM,
    FPGA_CLK_FREQ,
    NUM_TRANS_IN_UNIT,
    NUM_TRANS_IN_X,
    NUM_TRANS_IN_Y,
    TRANS_SPACING_MM,
)


class AUTD3:
    """AUTD3 device."""

    _pos: np.ndarray
    _rot: np.ndarray | None

    def __init__(self: "AUTD3", pos: ArrayLike) -> None:
        """Constructor.

        Arguments:
        ---------
            pos: Position of the device
        """
        self._pos = np.array(pos)
        self._rot = None

    def with_rotation(self: "AUTD3", rot: ArrayLike) -> "AUTD3":
        """Set device rotation.

        Arguments:
        ---------
            rot: Rotation of the device in quaternion
        """
        self._rot = np.array(rot)
        return self

    @staticmethod
    def transducer_spacing() -> float:
        """Spacing between transducers."""
        return TRANS_SPACING_MM

    @staticmethod
    def device_width() -> float:
        """Device width including substrate."""
        return DEVICE_WIDTH_MM

    @staticmethod
    def device_height() -> float:
        """Device height including substrate."""
        return DEVICE_HEIGHT_MM

    @staticmethod
    def num_transducer_in_x() -> int:
        """Number of transducer in x-axis of AUTD3 device."""
        return NUM_TRANS_IN_X

    @staticmethod
    def num_transducer_in_y() -> int:
        """Number of transducer in y-axis of AUTD3 device."""
        return NUM_TRANS_IN_Y

    @staticmethod
    def num_transducer_in_unit() -> int:
        """Number of transducer in an AUTD3 device."""
        return NUM_TRANS_IN_UNIT

    @staticmethod
    def fpga_clk_freq() -> int:
        """FPGA clock frequency."""
        return FPGA_CLK_FREQ
