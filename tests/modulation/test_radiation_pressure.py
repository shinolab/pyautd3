from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment
from pyautd3.driver.common.freq import Hz
from pyautd3.modulation import Sine
from pyautd3.modulation.radiation_pressure import RadiationPressure
from pyautd3.modulation.sine import SineOption
from pyautd3.modulation.static import Static
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_radiation_pressure():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = RadiationPressure(target=Sine(freq=150 * Hz, option=SineOption()))

        autd.send(m)

        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S0)
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
            assert autd.link().modulation_frequency_divide(dev.idx(), Segment.S0) == 10


def test_expected_radiation_pressure():
    assert Static(intensity=0xFF).expected_radiation_pressure() == 1.0
    assert Static(intensity=0x80).expected_radiation_pressure() == 0.25196465849876404
    assert RadiationPressure(Static(intensity=0x80)).expected_radiation_pressure() == 0.503821611404419
