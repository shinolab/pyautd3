from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import (
    ConfigurePhaseFilter,
    Controller,
    Phase,
)
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_phase_filter():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert np.all(autd.link.phase_filter(dev.idx) == 0x00)

        await autd.send_async(ConfigurePhaseFilter(lambda dev, tr: Phase((dev.idx + tr.idx) % 256)))

        for dev in autd.geometry:
            phase_filter = autd.link.phase_filter(dev.idx)
            for tr in dev:
                assert phase_filter[tr.idx] == (dev.idx + tr.idx) % 256
