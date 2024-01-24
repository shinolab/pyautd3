import numpy as np
import pytest

from pyautd3.modulation import Static
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller


@pytest.mark.asyncio()
async def test_static():
    async with create_controller() as autd:
        assert await autd.send_async(Static().with_intensity(0x80))

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx)
            mod_expect = [0x80] * 2
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx) == 0xFFFFFFFF


def test_static_default():
    m = Static()
    assert m.intensity().value == Base().modulation_static_default_intensity()
