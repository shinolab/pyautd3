import numpy as np
import pytest

from pyautd3.drive import Drive
from pyautd3.gain import TransducerTest
from pyautd3.geometry import Device, Transducer
from pyautd3.phase import Phase
from tests.test_autd import create_controller


@pytest.mark.asyncio()
async def test_transtest():
    async with create_controller() as autd:

        def f(dev: Device, tr: Transducer) -> Drive | None:
            if dev.idx == 0 and tr.idx == 0:
                return Drive(Phase(0x90), 0x80)
            if dev.idx == 1 and tr.idx == 248:
                return Drive(Phase(0x91), 0x81)
            return None

        assert await autd.send_async(TransducerTest(f))

        intensities, phases = autd.link.intensities_and_phases(0, 0)
        assert intensities[0] == 0x80
        assert phases[0] == 0x90
        assert np.all(intensities[1:-1] == 0)
        assert np.all(phases[1:-1] == 0)

        intensities, phases = autd.link.intensities_and_phases(1, 0)
        assert intensities[-1] == 0x81
        assert phases[-1] == 0x91
        assert np.all(intensities[:-1] == 0)
        assert np.all(phases[:-1] == 0)
