from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment
from pyautd3.modulation import Static
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_static():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Static.with_intensity(0x80)
        assert m.intensity == 0x80
        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [0x80] * 2
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 0xFFFFFFFF


def test_static_default():
    with create_controller() as autd:
        m = Static()
        assert Base().modulation_static_is_default(m._modulation_ptr(autd.geometry))
