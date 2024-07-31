from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment
from pyautd3.modulation.audio_file import Wav
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_wav():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Wav(Path(__file__).parent / "sin150.wav"))

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [
                128,
                157,
                185,
                210,
                230,
                245,
                253,
                254,
                248,
                236,
                217,
                194,
                167,
                137,
                109,
                80,
                54,
                32,
                15,
                5,
                1,
                5,
                15,
                32,
                54,
                80,
                109,
                137,
                167,
                194,
                217,
                236,
                248,
                254,
                253,
                245,
                230,
                210,
                185,
                157,
                128,
                99,
                71,
                46,
                26,
                11,
                3,
                2,
                8,
                20,
                39,
                62,
                89,
                119,
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
                119,
                89,
                62,
                39,
                20,
                8,
                2,
                3,
                11,
                26,
                46,
                71,
                99,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10
