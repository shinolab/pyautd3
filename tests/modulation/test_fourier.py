from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, Segment
from pyautd3.autd_error import AUTDError
from pyautd3.driver.common.freq import Hz
from pyautd3.modulation import Fourier, Sine
from pyautd3.modulation.fourier import FourierOption
from pyautd3.modulation.sine import SineOption
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_fourier_exact():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Fourier(
            components=(Sine(freq=x * Hz, option=SineOption()) for x in [50, 100, 150, 200, 250]),
            option=FourierOption(),
        )
        autd.send(m)

        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S0)
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
            assert autd.link().modulation_frequency_divide(dev.idx(), Segment.S0) == 10


def test_fourier_exact_float():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Fourier(
            components=(Sine(freq=x * Hz, option=SineOption()) for x in [50.0, 100.0, 150.0, 200.0, 250.0]),
            option=FourierOption(),
        )
        autd.send(m)

        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S0)
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
            assert autd.link().modulation_frequency_divide(dev.idx(), Segment.S0) == 10


def test_fourier_nearest():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Fourier(
            components=[Sine(freq=50.0 * Hz, option=SineOption()).into_nearest(), Sine(freq=100.0 * Hz, option=SineOption()).into_nearest()],
            option=FourierOption(),
        )
        autd.send(m)

        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S0)
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
            assert autd.link().modulation_frequency_divide(dev.idx(), Segment.S0) == 10


def test_fourier_clamp():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Fourier(
            components=[Sine(freq=200 * Hz, option=SineOption(offset=0x00))],
            option=FourierOption(clamp=False, scale_factor=None, offset=0x00),
        )
        with pytest.raises(AUTDError) as e:
            autd.send(m)
        assert str(e.value) == "Fourier modulation value (-1) is out of range [0, 255]"

    with create_controller() as autd:
        m = Fourier(
            components=[Sine(freq=200 * Hz, option=SineOption(offset=0x00))],
            option=FourierOption(clamp=True, scale_factor=None, offset=0x00),
        )
        autd.send(m)
        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S0)
            mod_expect = [0, 39, 74, 103, 121, 127, 121, 103, 74, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            assert np.array_equal(mod, mod_expect)

    with create_controller() as autd:
        m = Fourier(
            components=[Sine(freq=200 * Hz, option=SineOption(offset=0xFF))],
            option=FourierOption(clamp=False, scale_factor=2.0, offset=0x00),
        )
        with pytest.raises(AUTDError) as e:
            autd.send(m)
        assert str(e.value) == "Fourier modulation value (510) is out of range [0, 255]"
