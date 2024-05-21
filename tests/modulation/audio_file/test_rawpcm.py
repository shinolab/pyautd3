from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, SamplingConfig, Segment
from pyautd3.driver.defined.freq import Hz
from pyautd3.modulation.audio_file import RawPCM
from pyautd3.native_methods.autd3capi_modulation_audio_file import NativeMethods as AudioFile
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_rawpcm():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(RawPCM(Path(__file__).parent / "sin150.dat", 4000 * Hz))

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
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
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 5120

        autd.send(
            RawPCM(Path(__file__).parent / "sin150.dat", 4000 * Hz).with_sampling_config(
                SamplingConfig.Division(10240),
            ),
        )
        for dev in autd.geometry:
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10240


def test_rawpcm_default():
    with create_controller() as autd:
        m = RawPCM(Path(__file__), 4000 * Hz)
        assert AudioFile().modulation_raw_pcm_is_default(m._modulation_ptr(autd.geometry))
