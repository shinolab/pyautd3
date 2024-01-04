"""
File: static.py
Project: modulation
Created Date: 14/09/2023
Author: Shun Suzuki
-----
Last Modified: 29/09/2023
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2023 Shun Suzuki. All rights reserved.

"""

from pyautd3.emit_intensity import EmitIntensity
from pyautd3.internal.modulation import IModulation
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import ModulationPtr


class Static(IModulation):
    """Without modulation."""

    _intensity: EmitIntensity | None

    def __init__(self: "Static", intensity: int | EmitIntensity | None = None) -> None:
        super().__init__()
        self._intensity = intensity if intensity is None else EmitIntensity._cast(intensity)

    @staticmethod
    def with_intensity(intensity: int | EmitIntensity) -> "Static":
        """Static with intensity.

        Arguments:
        ---------
            intensity: Emission intensity
        """
        return Static(intensity)

    def _modulation_ptr(self: "Static") -> ModulationPtr:
        if self._intensity is not None:
            return Base().modulation_static_with_intensity(self._intensity.value)
        else:
            return Base().modulation_static()
