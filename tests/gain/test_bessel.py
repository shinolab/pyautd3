from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, EmitIntensity, Phase, Segment, rad
from pyautd3.gain import Bessel
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_bessel():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Bessel(autd.geometry.center, [0, 0, 1], np.pi / 4 * rad))
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert not np.all(phases == 0)

        g = Bessel(autd.geometry.center, [0, 0, 1], np.pi / 4 * rad).with_intensity(EmitIntensity(0x80)).with_phase_offset(Phase(0x90))
        autd.send(g)
        assert g.intensity == EmitIntensity(0x80)
        assert g.phase_offset == Phase(0x90)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


def test_bessel_default():
    g = Bessel([0, 0, 0], [0, 0, 1], np.pi / 4 * rad)
    assert np.array_equal(g.pos, [0, 0, 0])
    assert np.array_equal(g.dir, [0, 0, 1])
    assert g.theta == np.pi / 4 * rad
    assert Base().gain_bessel_is_default(g._gain_ptr(0))  # type: ignore [arg-type]
