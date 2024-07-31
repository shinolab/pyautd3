from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment
from pyautd3.driver.defined.freq import Hz
from pyautd3.modulation import Fourier, Sine
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_fourier_exact():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Fourier(Sine(x * Hz) for x in [50, 100, 150, 200, 250])
        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [
                127,
                156,
                183,
                205,
                220,
                227,
                226,
                219,
                205,
                188,
                170,
                153,
                139,
                129,
                124,
                123,
                127,
                133,
                140,
                147,
                152,
                155,
                154,
                151,
                145,
                138,
                131,
                125,
                120,
                118,
                119,
                122,
                127,
                132,
                137,
                140,
                141,
                141,
                137,
                133,
                127,
                121,
                116,
                113,
                112,
                113,
                117,
                121,
                127,
                131,
                134,
                135,
                133,
                129,
                122,
                115,
                108,
                102,
                99,
                99,
                101,
                106,
                113,
                120,
                127,
                130,
                129,
                124,
                115,
                100,
                83,
                65,
                48,
                35,
                27,
                26,
                34,
                48,
                70,
                97,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10


def test_fourier_exact_float():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Fourier(Sine(x * Hz) for x in [50.0, 100.0, 150.0, 200.0, 250.0])
        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [
                127,
                156,
                183,
                205,
                220,
                227,
                226,
                219,
                205,
                188,
                170,
                153,
                139,
                129,
                124,
                123,
                127,
                133,
                140,
                147,
                152,
                155,
                154,
                151,
                145,
                138,
                131,
                125,
                120,
                118,
                119,
                122,
                127,
                132,
                137,
                140,
                141,
                141,
                137,
                133,
                127,
                121,
                116,
                113,
                112,
                113,
                117,
                121,
                127,
                131,
                134,
                135,
                133,
                129,
                122,
                115,
                108,
                102,
                99,
                99,
                101,
                106,
                113,
                120,
                127,
                130,
                129,
                124,
                115,
                100,
                83,
                65,
                48,
                35,
                27,
                26,
                34,
                48,
                70,
                97,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10


def test_fourier_nearest():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Fourier([Sine.nearest(50.0 * Hz), Sine.nearest(100.0 * Hz)])
        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [
                127,
                142,
                156,
                171,
                184,
                196,
                207,
                217,
                225,
                231,
                236,
                238,
                239,
                238,
                235,
                231,
                225,
                218,
                209,
                200,
                191,
                180,
                170,
                160,
                150,
                141,
                132,
                124,
                118,
                112,
                108,
                105,
                104,
                103,
                104,
                106,
                109,
                113,
                117,
                122,
                127,
                132,
                136,
                141,
                145,
                147,
                149,
                150,
                150,
                148,
                146,
                141,
                136,
                129,
                121,
                113,
                104,
                94,
                83,
                73,
                63,
                53,
                44,
                36,
                29,
                23,
                18,
                15,
                15,
                15,
                18,
                22,
                29,
                36,
                46,
                57,
                70,
                83,
                97,
                112,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10
