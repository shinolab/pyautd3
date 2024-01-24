from pathlib import Path

import numpy as np
import pytest

from pyautd3 import SamplingConfiguration
from pyautd3.modulation.audio_file import RawPCM
from tests.test_autd import create_controller


@pytest.mark.asyncio()
async def test_rawpcm():
    with await create_controller() as autd:
        assert await autd.send_async(RawPCM(Path(__file__).parent / "sin150.dat", 4000))

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx)
            mod_expect = [
                157,
                185,
                210,
                231,
                245,
                253,
                255,
                249,
                236,
                218,
                194,
                167,
                138,
                108,
                79,
                53,
                31,
                14,
                4,
                0,
                4,
                14,
                31,
                53,
                79,
                108,
                138,
                167,
                194,
                218,
                236,
                249,
                255,
                253,
                245,
                231,
                210,
                185,
                157,
                128,
                98,
                70,
                45,
                24,
                10,
                2,
                0,
                6,
                19,
                37,
                61,
                88,
                117,
                147,
                176,
                202,
                224,
                241,
                251,
                255,
                251,
                241,
                224,
                202,
                176,
                147,
                117,
                88,
                61,
                37,
                19,
                6,
                0,
                2,
                10,
                24,
                45,
                70,
                98,
                128,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx) == 5120

        assert await autd.send_async(
            RawPCM(Path(__file__).parent / "sin150.dat", 4000).with_sampling_config(
                SamplingConfiguration.from_frequency_division(10240),
            ),
        )
        for dev in autd.geometry:
            assert autd.link.modulation_frequency_division(dev.idx) == 10240
