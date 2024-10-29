from collections.abc import Iterable
from typing import Self
import numpy as np
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.geometry import Geometry
from pyautd3.gain.holo.amplitude import Amplitude
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as GainHolo
from pyautd3.native_methods.structs import Vector3
from .constraint import EmissionConstraint
from .holo import Holo



class Greedy(Holo[Greedy]):
    def __init__(self, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> None: ...
    def _gain_ptr(self, _: Geometry) -> GainPtr: ...
    def with_phase_div(self, phase_div: int) -> Greedy: ...
    @property
    def phase_div(self) -> int: ...
