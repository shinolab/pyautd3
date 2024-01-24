import numpy as np
import pytest

from pyautd3 import Phase
from pyautd3.gain import Plane
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller


@pytest.mark.asyncio()
async def test_plane():
    with await create_controller() as autd:
        assert await autd.send_async(Plane([0, 0, 1]))
        for dev in autd.geometry:
            intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)

        assert await autd.send_async(Plane([0, 0, 1]).with_intensity(0x80).with_phase(Phase(0x81)))
        for dev in autd.geometry:
            intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x81)


def test_plane_default():
    g = Plane([0, 0, 1])
    assert np.array_equal(g.dir(), [0, 0, 1])
    assert g.intensity().value == Base().gain_plane_default_intensity()
    assert g.phase().value == Base().gain_plane_default_phase()
