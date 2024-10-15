from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, Segment
from pyautd3.autd_error import AUTDError
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
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            mod_expect = [
                128,
                157,
                184,
                206,
                221,
                228,
                227,
                219,
                206,
                189,
                171,
                154,
                140,
                130,
                125,
                124,
                128,
                134,
                141,
                148,
                153,
                156,
                155,
                152,
                146,
                139,
                132,
                126,
                121,
                119,
                120,
                123,
                128,
                133,
                137,
                141,
                142,
                141,
                138,
                133,
                128,
                122,
                117,
                114,
                113,
                114,
                118,
                122,
                128,
                132,
                135,
                136,
                134,
                129,
                123,
                116,
                109,
                103,
                100,
                99,
                102,
                107,
                114,
                121,
                127,
                131,
                130,
                125,
                115,
                101,
                84,
                66,
                49,
                36,
                28,
                27,
                34,
                49,
                71,
                98,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10


def test_fourier_exact_float():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Fourier(Sine(x * Hz) for x in [50.0, 100.0, 150.0, 200.0, 250.0])
        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            mod_expect = [
                128,
                157,
                184,
                206,
                221,
                228,
                227,
                219,
                206,
                189,
                171,
                154,
                140,
                130,
                125,
                124,
                128,
                134,
                141,
                148,
                153,
                156,
                155,
                152,
                146,
                139,
                132,
                126,
                121,
                119,
                120,
                123,
                128,
                133,
                137,
                141,
                142,
                141,
                138,
                133,
                128,
                122,
                117,
                114,
                113,
                114,
                118,
                122,
                128,
                132,
                135,
                136,
                134,
                129,
                123,
                116,
                109,
                103,
                100,
                99,
                102,
                107,
                114,
                121,
                127,
                131,
                130,
                125,
                115,
                101,
                84,
                66,
                49,
                36,
                28,
                27,
                34,
                49,
                71,
                98,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10


def test_fourier_nearest():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Fourier([Sine.nearest(50.0 * Hz), Sine.nearest(100.0 * Hz)])
        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            mod_expect = [
                128,
                142,
                157,
                171,
                185,
                197,
                208,
                218,
                226,
                232,
                236,
                239,
                240,
                239,
                236,
                231,
                226,
                218,
                210,
                201,
                191,
                181,
                171,
                161,
                151,
                141,
                133,
                125,
                118,
                113,
                109,
                106,
                104,
                104,
                105,
                107,
                110,
                113,
                118,
                123,
                128,
                132,
                137,
                142,
                145,
                148,
                150,
                151,
                151,
                149,
                146,
                142,
                137,
                130,
                122,
                114,
                104,
                94,
                84,
                74,
                64,
                54,
                45,
                37,
                29,
                24,
                19,
                16,
                15,
                16,
                19,
                23,
                29,
                37,
                47,
                58,
                70,
                84,
                98,
                113,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10


def test_fourier_clamp():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Fourier([Sine(200 * Hz).with_offset(0)]).with_clamp(False).with_scale_factor(None).with_offset(0)  # noqa: FBT003
        assert not m.clamp
        assert m.scale_factor is None
        assert m.offset == 0
        with pytest.raises(AUTDError) as e:
            autd.send(m)
        assert str(e.value) == "Fourier modulation value (-39) is out of range [0, 255]"

    with create_controller() as autd:
        m = Fourier([Sine(200 * Hz).with_offset(0)]).with_clamp(True).with_scale_factor(None).with_offset(0)  # noqa: FBT003
        autd.send(m)
        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            mod_expect = [0, 39, 75, 103, 121, 128, 121, 103, 75, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            assert np.array_equal(mod, mod_expect)

    with create_controller() as autd:
        m = Fourier([Sine(200 * Hz).with_offset(0xFF)]).with_clamp(False).with_scale_factor(2.0).with_offset(0)  # noqa: FBT003
        assert not m.clamp
        with pytest.raises(AUTDError) as e:
            autd.send(m)
        assert str(e.value) == "Fourier modulation value (334) is out of range [0, 255]"
