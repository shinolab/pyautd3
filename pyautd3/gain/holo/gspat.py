import ctypes
from collections.abc import Iterable
from typing import Self

import numpy as np

from pyautd3.derive import builder, datagram, gain
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.geometry import Geometry
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.gain.holo.backend import Backend
from pyautd3.gain.holo.constraint import EmissionConstraint
from pyautd3.gain.holo.holo import HoloWithBackend
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3


@datagram
@datagram_with_segment
@gain
@builder
class GSPAT(HoloWithBackend["GSPAT"]):
    _param_repeat: int

    def __init__(self: Self, backend: Backend, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> None:
        super().__init__(EmissionConstraint.Clamp(0x00, 0xFF), backend, iterable)
        self._param_repeat = 100

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci = np.fromiter((np.void(Vector3(d)) for d in self._foci), dtype=Vector3)  # type: ignore[type-var,call-overload]
        amps = np.fromiter((d.pascal for d in self._amps), dtype=ctypes.c_float)  # type: ignore[type-var,call-overload]
        return self._backend._gspat(
            foci.ctypes.data_as(ctypes.POINTER(Vector3)),  # type: ignore[arg-type]
            amps.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
            size,
            self._param_repeat,
            self._constraint,
        )
