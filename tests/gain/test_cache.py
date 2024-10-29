from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, EmitIntensity, Phase, Segment
from pyautd3.gain import Uniform
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_cache():
    autd: Controller[Audit]
    with create_controller() as autd:
        g = Uniform((EmitIntensity(0x80), Phase(0x90))).with_cache()
        autd.send(g)
        autd.send(g)

        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x90)

    _ = Uniform((EmitIntensity(0x80), Phase(0x90))).with_cache()
