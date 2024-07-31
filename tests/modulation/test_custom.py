from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, SamplingConfig, Segment
from pyautd3.modulation import Custom
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_modulation_custom():
    autd: Controller[Audit]
    with create_controller() as autd:
        buf = np.array([0] * 10)
        buf[0] = 0xFF
        m = Custom(buf, SamplingConfig(10))

        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            assert len(mod) == 10
            assert mod[0] == 0xFF
            assert np.all(mod[1:] == 0)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10
