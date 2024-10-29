from collections.abc import Iterable
from typing import Self
import numpy as np
from pyautd3.driver.geometry import Geometry
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3
from .backend import Backend
from .constraint import EmissionConstraint
from .holo import HoloWithBackend



class GSPAT(HoloWithBackend[GSPAT]):
    def __init__(self, backend: Backend, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> None: ...
    def _gain_ptr(self, _: Geometry) -> GainPtr: ...
    def with_repeat(self, repeat: int) -> GSPAT: ...
    @property
    def repeat(self) -> int: ...
