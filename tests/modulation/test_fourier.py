from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, Segment
from pyautd3.modulation import Fourier, Sine
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_fourier():
    autd: Controller[Audit]
    with await create_controller() as autd:
        m = Fourier(Sine(50)).add_components_from_iter(Sine(x) for x in [100, 150]) + Sine(200) + Sine(250)
        assert await autd.send_async(m)

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [
                127,
                156,
                183,
                205,
                220,
                227,
                226,
                219,
                205,
                188,
                170,
                153,
                139,
                129,
                124,
                123,
                127,
                133,
                140,
                147,
                152,
                155,
                154,
                151,
                145,
                138,
                131,
                125,
                120,
                118,
                119,
                122,
                127,
                132,
                137,
                140,
                141,
                141,
                137,
                133,
                127,
                121,
                116,
                113,
                112,
                113,
                117,
                121,
                127,
                131,
                134,
                135,
                133,
                129,
                122,
                115,
                108,
                102,
                99,
                99,
                101,
                106,
                113,
                120,
                127,
                130,
                129,
                124,
                115,
                100,
                83,
                65,
                48,
                35,
                27,
                26,
                34,
                48,
                70,
                97,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 5120
