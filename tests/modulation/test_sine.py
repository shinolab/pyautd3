from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, EmitIntensity, Phase, SamplingConfiguration, Segment
from pyautd3.autd_error import AUTDError
from pyautd3.modulation import SamplingMode, Sine
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_sine():
    autd: Controller[Audit]
    with await create_controller() as autd:
        m = Sine(150).with_intensity(EmitIntensity.maximum() // 2).with_offset(EmitIntensity.maximum() // 4).with_phase(Phase.from_rad(np.pi / 2))
        assert m.freq() == 150
        assert m.intensity() == EmitIntensity.maximum() // 2
        assert m.offset() == EmitIntensity.maximum() // 4
        assert m.phase() == Phase.from_rad(np.pi / 2)
        assert await autd.send_async(m)

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [
                127,
                125,
                120,
                111,
                100,
                87,
                73,
                58,
                43,
                30,
                18,
                9,
                3,
                0,
                0,
                4,
                12,
                22,
                34,
                48,
                63,
                78,
                92,
                104,
                114,
                122,
                126,
                126,
                123,
                117,
                108,
                96,
                83,
                68,
                53,
                39,
                26,
                15,
                6,
                1,
                0,
                1,
                6,
                15,
                26,
                39,
                53,
                68,
                83,
                96,
                108,
                117,
                123,
                126,
                126,
                122,
                114,
                104,
                92,
                78,
                63,
                48,
                34,
                22,
                12,
                4,
                0,
                0,
                3,
                9,
                18,
                30,
                43,
                58,
                73,
                87,
                100,
                111,
                120,
                125,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 5120

        assert await autd.send_async(
            Sine(150).with_sampling_config(
                SamplingConfiguration.from_frequency_division(10240),
            ),
        )
        for dev in autd.geometry:
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10240


@pytest.mark.asyncio()
async def test_sine_mode():
    autd: Controller[Audit]
    with await create_controller() as autd:
        m = Sine(150).with_mode(SamplingMode.SizeOptimized)
        assert m.mode() == SamplingMode.SizeOptimized
        assert await autd.send_async(m)
        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [127, 156, 184, 209, 229, 244, 253, 254, 249, 237, 220, 197, 171, 142, 112, 83, 57, 34, 17, 5, 0, 1, 10, 25, 45, 70, 98]
            assert np.array_equal(mod, mod_expect)

        with pytest.raises(AUTDError):
            await autd.send_async(Sine(100.1).with_mode(SamplingMode.ExactFrequency))

        assert await autd.send_async(Sine(100.1).with_mode(SamplingMode.SizeOptimized))


def test_sine_default():
    m = Sine(150.0)
    assert m.freq() == 150.0
    assert Base().modulation_sine_is_default(m._modulation_ptr())
