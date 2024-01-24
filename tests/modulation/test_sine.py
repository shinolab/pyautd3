import numpy as np
import pytest

from pyautd3 import EmitIntensity, Phase, SamplingConfiguration
from pyautd3.autd_error import AUTDError
from pyautd3.modulation import SamplingMode, Sine
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import NativeMethods as Def
from tests.test_autd import create_controller


@pytest.mark.asyncio()
async def test_sine():
    async with create_controller() as autd:
        assert await autd.send_async(
            Sine(150).with_intensity(EmitIntensity.maximum() // 2).with_offset(EmitIntensity.maximum() // 4).with_phase(Phase.from_rad(np.pi / 2)),
        )

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx)
            mod_expect = [
                126,
                124,
                119,
                111,
                100,
                87,
                73,
                58,
                44,
                30,
                18,
                9,
                3,
                0,
                1,
                5,
                12,
                22,
                34,
                48,
                63,
                78,
                92,
                104,
                114,
                121,
                125,
                126,
                123,
                117,
                108,
                96,
                82,
                68,
                53,
                39,
                26,
                15,
                7,
                2,
                0,
                2,
                7,
                15,
                26,
                39,
                53,
                68,
                82,
                96,
                108,
                117,
                123,
                126,
                125,
                121,
                114,
                104,
                92,
                78,
                63,
                48,
                34,
                22,
                12,
                5,
                1,
                0,
                3,
                9,
                18,
                30,
                44,
                58,
                73,
                87,
                100,
                111,
                119,
                124,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx) == 5120

        assert await autd.send_async(
            Sine(150).with_sampling_config(
                SamplingConfiguration.from_frequency_division(10240),
            ),
        )
        for dev in autd.geometry:
            assert autd.link.modulation_frequency_division(dev.idx) == 10240


@pytest.mark.asyncio()
async def test_sine_mode():
    async with create_controller() as autd:
        assert await autd.send_async(Sine(150).with_mode(SamplingMode.SizeOptimized))
        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx)
            mod_expect = [127, 156, 184, 209, 229, 244, 252, 254, 249, 237, 219, 197, 170, 142, 112, 84, 57, 35, 17, 5, 0, 2, 10, 25, 45, 70, 98]
            assert np.array_equal(mod, mod_expect)

        with pytest.raises(AUTDError):
            await autd.send_async(Sine(100.1).with_mode(SamplingMode.ExactFrequency))

        assert await autd.send_async(Sine(100.1).with_mode(SamplingMode.SizeOptimized))


def test_sine_default():
    m = Sine(150.0)
    assert m.freq() == 150.0
    assert m.intensity().value == Base().modulation_sine_default_intensity()
    assert m.offset().value == Base().modulation_sine_default_offset()
    assert m.phase().value == Base().modulation_sine_default_phase()
    assert m.mode().value == Base().modulation_sine_default_mode()
    assert Def().sampling_config_eq(
        m.sampling_config._internal,
        Base().modulation_sine_default_sampling_config(),
    )
