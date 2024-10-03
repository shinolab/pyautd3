from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, SamplingConfig, Segment, kHz
from pyautd3.modulation import Custom
from pyautd3.modulation.resample import Rectangular, SincInterpolation
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_modulation_custom():
    autd: Controller[Audit]
    with create_controller() as autd:
        buf = np.array([0] * 10)
        buf[0] = 0xFF
        m = Custom(buf, SamplingConfig(10))

        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            assert len(mod) == 10
            assert mod[0] == 0xFF
            assert np.all(mod[1:] == 0)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10


def test_modulation_custom_with_resample():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Custom.new_with_resample([127, 255, 127, 0], 2.0 * kHz, 4.0 * kHz, SincInterpolation())

        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            assert np.array_equal([127, 217, 255, 217, 127, 37, 0, 37], mod)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10

    with create_controller() as autd:
        m = Custom.new_with_resample([127, 255, 127, 0], 2.0 * kHz, 4.0 * kHz, SincInterpolation(Rectangular(32)))

        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            assert np.array_equal([127, 217, 255, 223, 127, 42, 0, 37], mod)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10
