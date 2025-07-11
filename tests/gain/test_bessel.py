from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Intensity, Phase, Segment, rad
from pyautd3.gain import Bessel
from pyautd3.gain.bessel import BesselOption
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_bessel():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Bessel(pos=autd.center(), direction=[0, 0, 1], theta=np.pi / 4 * rad, option=BesselOption()))
        for dev in autd.geometry():
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert not np.all(phases == 0)

        g = Bessel(
            pos=autd.center(),
            direction=[0, 0, 1],
            theta=np.pi / 4 * rad,
            option=BesselOption(
                intensity=Intensity(0x80),
                phase_offset=Phase(0x90),
            ),
        )
        autd.send(g)
        for dev in autd.geometry():
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


def test_bessel_default():
    assert Base().gain_bessel_is_default(BesselOption()._inner())
