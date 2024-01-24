import numpy as np
import pytest

from pyautd3.gain import Null
from tests.test_autd import create_controller


@pytest.mark.asyncio()
async def test_null():
    with await create_controller() as autd:
        assert await autd.send_async(Null())

        for dev in autd.geometry:
            intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
            assert np.all(intensities == 0)
            assert np.all(phases == 0)
