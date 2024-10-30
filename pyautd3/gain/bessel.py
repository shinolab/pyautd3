from typing import Self

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.derive import builder, datagram, gain
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.defined.angle import Angle
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr
from pyautd3.native_methods.structs import Vector3


@datagram
@datagram_with_segment
@gain
@builder
class Bessel(Gain):
    _param_pos: np.ndarray
    _param_dir: np.ndarray
    _param_theta: Angle
    _param_intensity: EmitIntensity
    _param_phase_offset: Phase

    def __init__(self: Self, pos: ArrayLike, direction: ArrayLike, theta: Angle) -> None:
        super().__init__()
        self._param_pos = np.array(pos)
        self._param_dir = np.array(direction)
        self._param_theta = theta
        self._param_intensity = EmitIntensity.maximum()
        self._param_phase_offset = Phase(0)

    def _gain_ptr(self: Self, _: Geometry) -> GainPtr:
        return Base().gain_bessel(
            Vector3(self._param_pos),
            Vector3(self._param_dir),
            self._param_theta.radian,
            self._param_intensity.value,
            self._param_phase_offset.value,
        )
