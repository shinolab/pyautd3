from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, Segment
from pyautd3.gain import Focus
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_focus():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert await autd.send_async(Focus(autd.geometry.center))
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert not np.all(phases == 0)

        assert await autd.send_async(Focus(autd.geometry.center).with_intensity(0x80))
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


def test_focus_default():
    g = Focus([0, 0, 0])
    assert np.array_equal(g.pos(), [0, 0, 0])
    assert Base().gain_focus_is_default(g._gain_ptr(0))  # type: ignore [arg-type]
