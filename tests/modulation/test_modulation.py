from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment
from pyautd3.driver.defined.freq import Hz
from pyautd3.modulation import Modulation
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


class Burst(Modulation):
    def __init__(self: "Burst") -> None:
        super().__init__(4000 * Hz)

    def calc(self: "Burst"):
        buf = np.array([0] * 10)
        buf[0] = 0xFF
        return buf


def test_modulation():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Burst()

        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            assert len(mod) == 10
            assert mod[0] == 0xFF
            assert np.all(mod[1:] == 0)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10
