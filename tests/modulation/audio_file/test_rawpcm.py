from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment, kHz
from pyautd3.driver.defined.freq import Hz
from pyautd3.modulation.audio_file import RawPCM
from pyautd3.modulation.resample import SincInterpolation
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_rawpcm():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(RawPCM(Path(__file__).parent / "sin150.dat", 4000 * Hz))

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
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
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10

        autd.send(RawPCM(Path(__file__).parent / "sin150.dat", 2000 * Hz))
        for dev in autd.geometry:
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 20


def test_rawpcm_with_resample():
    autd: Controller[Audit]
    with create_controller() as autd:
        expect = [127, 217, 255, 217, 127, 37, 0, 37]
        buf = [127, 255, 127, 0]

        with Path.open(Path(__file__).parent / "custom.dat", "wb") as f:
            for b in buf:
                f.write(b.to_bytes(1, byteorder="little"))

        autd.send(RawPCM.new_with_resample(Path(__file__).parent / "custom.dat", 2.0 * kHz, 4 * kHz, SincInterpolation()))

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            assert np.array_equal(expect, mod)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10
