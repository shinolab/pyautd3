from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, SamplingConfiguration, Segment
from pyautd3.autd_error import AUTDError
from pyautd3.modulation import SamplingMode, Square
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_square():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert await autd.send_async(Square(200).with_low(32).with_high(85).with_duty(0.1))

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [85, 85, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 5120

        assert await autd.send_async(
            Square(150).with_sampling_config(
                SamplingConfiguration.from_frequency_division(10240),
            ),
        )
        for dev in autd.geometry:
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10240


@pytest.mark.asyncio()
async def test_square_mode():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert await autd.send_async(Square(150).with_mode(SamplingMode.SizeOptimized))
        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            assert np.array_equal(mod, mod_expect)

        with pytest.raises(AUTDError):
            await autd.send_async(Square(100.1).with_mode(SamplingMode.ExactFrequency))

        assert await autd.send_async(Square(100.1).with_mode(SamplingMode.SizeOptimized))


def test_square_default():
    m = Square(150.0)
    assert m.freq() == 150.0
    assert Base().modulation_square_is_default(m._modulation_ptr())
