import wave
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment, kHz
from pyautd3.modulation.audio_file import Wav
from pyautd3.modulation.resample import SincInterpolation
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_wav():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Wav(Path(__file__).parent / "sin150.wav"))

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
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


def test_wav_with_resample():
    autd: Controller[Audit]
    with create_controller() as autd:
        expect = [127, 217, 255, 217, 127, 37, 0, 37]
        buf = [127, 255, 127, 0]

        with wave.open(str(Path(__file__).parent / "custom.wav"), "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(1)
            f.setframerate(2000)
            f.setnframes(len(buf))
            f.writeframes(np.array(buf, dtype=np.uint8).tobytes())

        autd.send(Wav.new_with_resample(Path(__file__).parent / "custom.wav", 4 * kHz, SincInterpolation()))

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            assert np.array_equal(expect, mod)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10
