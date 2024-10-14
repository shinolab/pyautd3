from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment, Static
from pyautd3.driver.datagram.segment import SwapSegment
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.modulation import Modulation, Sine
from pyautd3.modulation.fourier import Fourier
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_cache():
    autd1: Controller[Audit]
    autd2: Controller[Audit]
    with create_controller() as autd1, create_controller() as autd2:
        m1 = Sine(150 * Hz)
        m2 = Sine(150 * Hz).with_cache()

        autd1.send(m1)
        autd2.send(m2)

        for dev in autd1.geometry:
            mod_expect = autd1._link.modulation_buffer(dev.idx, Segment.S0)
            mod = autd2._link.modulation_buffer(dev.idx, Segment.S0)
            assert np.array_equal(mod, mod_expect)
            assert autd2._link.modulation_frequency_division(dev.idx, Segment.S0) == 10

        mod1 = autd1._link.modulation_buffer(0, Segment.S0)
        mod2 = autd2._link.modulation_buffer(0, Segment.S0)
        assert np.array_equal(mod1, mod2)


class CacheTest(Modulation["CacheTest"]):
    calc_cnt: int

    def __init__(self: "CacheTest") -> None:
        super().__init__(4000 * Hz)
        self.calc_cnt = 0

    def calc(self: "CacheTest"):
        self.calc_cnt += 1
        return np.array([0xFF] * 2)


def test_cache_check_once():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = CacheTest()
        autd.send(m)
        assert m.calc_cnt == 1
        autd.send(m)
        assert m.calc_cnt == 2

        m = CacheTest()
        m_cached = m.with_cache()

        autd.send(m_cached)
        assert m.calc_cnt == 1
        autd.send(m_cached)
        assert m.calc_cnt == 1


def test_radiation_pressure():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Sine(150 * Hz).with_radiation_pressure()

        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            mod_expect = [
                181,
                200,
                217,
                231,
                243,
                250,
                254,
                255,
                252,
                245,
                236,
                222,
                206,
                188,
                166,
                142,
                116,
                89,
                60,
                32,
                0,
                32,
                60,
                89,
                116,
                142,
                166,
                188,
                206,
                222,
                236,
                245,
                252,
                255,
                254,
                250,
                243,
                231,
                217,
                200,
                181,
                158,
                134,
                107,
                78,
                50,
                23,
                0,
                39,
                70,
                97,
                125,
                150,
                173,
                194,
                212,
                227,
                239,
                248,
                253,
                255,
                253,
                248,
                239,
                227,
                212,
                194,
                173,
                150,
                125,
                97,
                70,
                39,
                0,
                23,
                50,
                78,
                107,
                134,
                158,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10


def test_fir():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Fourier([Sine(50 * Hz), Sine(1000 * Hz)]).with_fir(
            [
                0.0,
                2.336_732_5e-6,
                8.982_681e-6,
                1.888_706_2e-5,
                3.030_097e-5,
                4.075_849e-5,
                4.708_182e-5,
                4.542_212e-5,
                3.134_882_4e-5,
                0.0,
                -5.369_572_3e-5,
                -0.000_134_718_74,
                -0.000_247_578_05,
                -0.000_395_855_98,
                -0.000_581_690_7,
                -0.000_805_217_2,
                -0.001_063_996,
                -0.001_352_463_7,
                -0.001_661_447_3,
                -0.001_977_784_6,
                -0.002_284_095_4,
                -0.002_558_745,
                -0.002_776_031,
                -0.002_906_624_2,
                -0.002_918_272_5,
                -0.002_776_767_4,
                -0.002_447_156_7,
                -0.001_895_169_7,
                -0.001_088_802_4,
                0.0,
                0.001_393_638_8,
                0.003_107_224_6,
                0.005_147_092_5,
                0.007_509_561,
                0.010_180_013,
                0.013_132_379,
                0.016_329_063,
                0.019_721_36,
                0.023_250_382,
                0.026_848_452,
                0.030_440_966,
                0.033_948_626,
                0.037_290_003,
                0.040_384_263,
                0.043_154_005,
                0.045_528_06,
                0.047_444_11,
                0.048_851_013,
                0.049_710_777,
                0.05,
                0.049_710_777,
                0.048_851_013,
                0.047_444_11,
                0.045_528_06,
                0.043_154_005,
                0.040_384_263,
                0.037_290_003,
                0.033_948_626,
                0.030_440_966,
                0.026_848_452,
                0.023_250_382,
                0.019_721_36,
                0.016_329_063,
                0.013_132_379,
                0.010_180_013,
                0.007_509_561,
                0.005_147_092_5,
                0.003_107_224_6,
                0.001_393_638_8,
                0.0,
                -0.001_088_802_4,
                -0.001_895_169_7,
                -0.002_447_156_7,
                -0.002_776_767_4,
                -0.002_918_272_5,
                -0.002_906_624_2,
                -0.002_776_031,
                -0.002_558_745,
                -0.002_284_095_4,
                -0.001_977_784_6,
                -0.001_661_447_3,
                -0.001_352_463_7,
                -0.001_063_996,
                -0.000_805_217_2,
                -0.000_581_690_7,
                -0.000_395_855_98,
                -0.000_247_578_05,
                -0.000_134_718_74,
                -5.369_572_3e-5,
                0.0,
                3.134_882_4e-5,
                4.542_212e-5,
                4.708_182e-5,
                4.075_849e-5,
                3.030_097e-5,
                1.888_706_2e-5,
                8.982_681e-6,
                2.336_732_5e-6,
                0.0,
            ],
        )

        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            mod_expect = [
                127,
                131,
                136,
                140,
                145,
                149,
                153,
                157,
                161,
                164,
                168,
                171,
                173,
                176,
                178,
                180,
                182,
                183,
                184,
                184,
                184,
                184,
                184,
                183,
                182,
                180,
                178,
                176,
                173,
                171,
                168,
                164,
                161,
                157,
                153,
                149,
                145,
                140,
                136,
                131,
                127,
                122,
                118,
                113,
                109,
                105,
                100,
                96,
                93,
                89,
                86,
                83,
                80,
                77,
                75,
                73,
                72,
                70,
                70,
                69,
                69,
                69,
                70,
                70,
                72,
                73,
                75,
                77,
                80,
                83,
                86,
                89,
                93,
                96,
                100,
                105,
                109,
                113,
                118,
                122,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10


def test_mod_segment():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link.current_mod_segment(0) == Segment.S0

        autd.send(Static.with_intensity(0x01))
        assert autd.link.current_mod_segment(0) == Segment.S0
        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            assert np.all(mod == 0x01)
        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S1)
            assert np.all(mod == 0xFF)

        autd.send(Static.with_intensity(0x02).with_segment(Segment.S1, TransitionMode.Immediate))
        assert autd.link.current_mod_segment(0) == Segment.S1
        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            assert np.all(mod == 0x01)
        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S1)
            assert np.all(mod == 0x02)

        autd.send(Static.with_intensity(0x03).with_segment(Segment.S0, None))
        assert autd.link.current_mod_segment(0) == Segment.S1
        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            assert np.all(mod == 0x03)
        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S1)
            assert np.all(mod == 0x02)

        autd.send(SwapSegment.Modulation(Segment.S0, TransitionMode.Immediate))
        assert autd.link.current_mod_segment(0) == Segment.S0
