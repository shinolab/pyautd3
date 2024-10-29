from typing import Self
import numpy as np
from numpy.typing import ArrayLike
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3



class Focus(Gain[Focus]):
    def __init__(self, pos: ArrayLike) -> None: ...
    def _gain_ptr(self, _: Geometry) -> GainPtr: ...
    def with_intensity(self, intensity: EmitIntensity) -> Focus: ...
    def with_phase_offset(self, phase_offset: Phase) -> Focus: ...
    @property
    def pos(self) -> np.ndarray: ...
    @property
    def intensity(self) -> EmitIntensity: ...
    @property
    def phase_offset(self) -> Phase: ...
