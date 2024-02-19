from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, Segment
from pyautd3.driver.common.drive import Drive
from pyautd3.driver.common.phase import Phase
from pyautd3.driver.geometry import Device, Transducer
from pyautd3.gain import TransducerTest
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_transtest():
    autd: Controller[Audit]
    with await create_controller() as autd:

        def f(dev: Device, tr: Transducer) -> Drive | None:
            if dev.idx == 0 and tr.idx == 0:
                return Drive(Phase(0x90), 0x80)
            if dev.idx == 1 and tr.idx == 248:
                return Drive(Phase(0x91), 0x81)
            return None

        assert await autd.send_async(TransducerTest(f))

        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert intensities[0] == 0x80
        assert phases[0] == 0x90
        assert np.all(intensities[1:-1] == 0)
        assert np.all(phases[1:-1] == 0)

        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert intensities[-1] == 0x81
        assert phases[-1] == 0x91
        assert np.all(intensities[:-1] == 0)
        assert np.all(phases[:-1] == 0)
