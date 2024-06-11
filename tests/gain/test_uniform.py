from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, EmitIntensity, Segment
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.gain import Uniform
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_uniform():
    autd: Controller[Audit]
    with create_controller() as autd:
        g = Uniform(0x80).with_phase(0x90)
        assert g.intensity == EmitIntensity(0x80)
        assert g.phase == Phase(0x90)
        autd.send(g)

        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x90)


def test_bessel_default():
    g = Uniform(0x00)
    assert g.intensity.value == 0x00
    assert Base().gain_uniform_is_default(g._gain_ptr(0))  # type: ignore [arg-type]
