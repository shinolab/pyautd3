from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, EmitIntensity, Phase, Segment
from pyautd3.gain import Plane
from pyautd3.gain.plane import PlaneOption
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_plane():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Plane(direction=[0, 0, 1], option=PlaneOption()))
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)

        g = Plane(direction=[0, 0, 1], option=PlaneOption(intensity=EmitIntensity(0x80), phase_offset=Phase(0x81)))
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x81)


def test_plane_default():
    assert Base().gain_planel_is_default(PlaneOption()._inner())
