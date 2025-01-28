from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, EmitIntensity, Phase, Segment
from pyautd3.gain import Focus
from pyautd3.gain.focus import FocusOption
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_focus():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Focus(pos=autd.center, option=FocusOption()))
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert not np.all(phases == 0)

        g = Focus(pos=autd.center, option=FocusOption(intensity=EmitIntensity(0x80), phase_offset=Phase(0x90)))
        autd.send(g)
        assert np.array_equal(g.pos, autd.center)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


def test_focus_default():
    assert Base().gain_focus_is_default(FocusOption()._inner())
