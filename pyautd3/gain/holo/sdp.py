import ctypes
from collections.abc import Iterable

import numpy as np

from pyautd3.driver.geometry import Geometry
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3

from .backend import Backend
from .constraint import EmissionConstraint
from .holo import HoloWithBackend


class SDP(HoloWithBackend["SDP"]):
    _alpha: float
    _lambda: float
    _repeat: int

    def __init__(self: "SDP", backend: Backend, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> None:
        super().__init__(EmissionConstraint.DontCare, backend, iterable)
        self._alpha = 1e-3
        self._lambda = 0.9
        self._repeat = 100

    def with_alpha(self: "SDP", alpha: float) -> "SDP":
        self._alpha = alpha
        return self

    @property
    def alpha(self: "SDP") -> float:
        return self._alpha

    def with_lambda(self: "SDP", lambda_: float) -> "SDP":
        self._lambda = lambda_
        return self

    @property
    def lambda_(self: "SDP") -> float:
        return self._lambda

    def with_repeat(self: "SDP", repeat: int) -> "SDP":
        self._repeat = repeat
        return self

    @property
    def repeat(self: "SDP") -> int:
        return self._repeat

    def _gain_ptr(self: "SDP", _: Geometry) -> GainPtr:
        size = len(self._amps)
        foci = np.fromiter((np.void(Vector3(d)) for d in self._foci), dtype=Vector3)  # type: ignore[type-var,call-overload]
        amps = np.fromiter((d.pascal for d in self._amps), dtype=ctypes.c_float)  # type: ignore[type-var,call-overload]
        return self._backend._sdp(
            foci.ctypes.data_as(ctypes.POINTER(Vector3)),  # type: ignore[arg-type]
            amps.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
            size,
            self._alpha,
            self._lambda,
            self._repeat,
            self._constraint,
        )
