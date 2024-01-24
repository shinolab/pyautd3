import numpy as np
import pytest

from pyautd3.gain import Bessel
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller


@pytest.mark.asyncio()
async def test_bessel():
    async with create_controller() as autd:
        assert await autd.send_async(Bessel(autd.geometry.center, [0, 0, 1], np.pi / 4))
        for dev in autd.geometry:
            intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
            assert np.all(intensities == 0xFF)
            assert not np.all(phases == 0)

        assert await autd.send_async(Bessel(autd.geometry.center, [0, 0, 1], np.pi / 4).with_intensity(0x80))
        for dev in autd.geometry:
            intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


def test_bessel_default():
    g = Bessel([0, 0, 0], [0, 0, 1], np.pi / 4)
    assert np.array_equal(g.pos(), [0, 0, 0])
    assert np.array_equal(g.dir(), [0, 0, 1])
    assert g.theta() == np.pi / 4
    assert g.intensity().value == Base().gain_bessel_default_intensity()
