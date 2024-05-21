from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, EmitIntensity, Phase, Segment
from pyautd3.gain import Plane
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_plane():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Plane([0, 0, 1]))
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)

        g = Plane([0, 0, 1]).with_intensity(EmitIntensity(0x80)).with_phase_offset(Phase(0x81))
        assert np.array_equal(g.dir, [0, 0, 1])
        assert g.intensity == EmitIntensity(0x80)
        assert g.phase_offset == Phase(0x81)
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x81)


def test_plane_default():
    g = Plane([0, 0, 1])
    assert np.array_equal(g.dir, [0, 0, 1])
    assert Base().gain_planel_is_default(g._gain_ptr(0))  # type: ignore [arg-type]
