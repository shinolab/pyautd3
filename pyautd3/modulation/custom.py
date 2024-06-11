import ctypes

import numpy as np

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr, SamplingConfigWrap


class Custom(Modulation["Custom"]):
    _buf: np.ndarray

    def __init__(self: "Custom", buf: np.ndarray, config: SamplingConfigWrap) -> None:
        super().__init__(config)
        self._buf = buf

    def _modulation_ptr(self: "Custom", _: Geometry) -> ModulationPtr:
        return Base().modulation_raw(
            self._config,
            self._loop_behavior,
            self._buf.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
            len(self._buf),
        )
