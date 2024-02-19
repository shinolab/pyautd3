from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, EmitIntensity, LoopBehavior, SamplingConfiguration, Segment
from pyautd3.modulation import Modulation
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


class Burst(Modulation):
    def __init__(self: "Burst") -> None:
        super().__init__(SamplingConfiguration.from_frequency(4e3), LoopBehavior.infinite())

    def calc(self: "Burst"):
        buf = np.array([EmitIntensity(0)] * 10)
        buf[0] = EmitIntensity(0xFF)
        return buf


@pytest.mark.asyncio()
async def test_modulation():
    autd: Controller[Audit]
    with await create_controller() as autd:
        m = Burst()

        assert m.sampling_config.frequency == 4e3
        assert len(m) == 10

        assert await autd.send_async(m)

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            assert len(mod) == 10
            assert mod[0] == 0xFF
            assert np.all(mod[1:] == 0)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 5120
