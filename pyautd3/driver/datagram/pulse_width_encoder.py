import ctypes

import numpy as np

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.native_methods.utils import _validate_ptr

from .datagram import Datagram


class PulseWidthEncoder(Datagram):
    _buf: np.ndarray | None

    def __init__(self: "PulseWidthEncoder", buf: np.ndarray | None = None) -> None:
        super().__init__()
        self._buf = buf

    def _datagram_ptr(self: "PulseWidthEncoder", _: Geometry) -> DatagramPtr:
        return (
            Base().datagram_pulse_width_encoder_default()
            if self._buf is None
            else _validate_ptr(
                Base().datagram_pulse_width_encoder(
                    self._buf.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16)),  # type: ignore [arg-type]
                    len(self._buf),
                ),
            )
        )
