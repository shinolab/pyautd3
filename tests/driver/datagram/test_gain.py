from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, EmitIntensity, Phase, Segment, SwapSegment
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.gain import Uniform
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_cache():
    autd: Controller[Audit]
    with create_controller() as autd:
        g = Uniform((EmitIntensity(0x80), Phase(0x90))).with_cache()
        autd.send(g)
        autd.send(g)

        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x90)

    _ = Uniform((EmitIntensity(0x80), Phase(0x90))).with_cache()


def test_gain_segment():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link.current_stm_segment(0) == Segment.S0

        autd.send(Uniform((EmitIntensity(0x01), Phase(0x02))))
        assert autd.link.current_stm_segment(0) == Segment.S0
        assert autd.link.stm_cycle(0, Segment.S0) == 1
        assert autd.link.stm_freqency_division(0, Segment.S0) == 0xFFFF
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x01)
            assert np.all(phases == 0x02)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x00)
            assert np.all(phases == 0x00)

        autd.send(Uniform((EmitIntensity(0x03), Phase(0x04))).with_segment(Segment.S1, TransitionMode.Immediate))
        assert autd.link.current_stm_segment(0) == Segment.S1
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x01)
            assert np.all(phases == 0x02)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x03)
            assert np.all(phases == 0x04)

        autd.send(Uniform((EmitIntensity(0x05), Phase(0x06))).with_segment(Segment.S0, None))
        assert autd.link.current_stm_segment(0) == Segment.S1
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x05)
            assert np.all(phases == 0x06)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S1, 0)
            assert np.all(intensities == 0x03)
            assert np.all(phases == 0x04)

        autd.send(SwapSegment.Gain(Segment.S0, TransitionMode.Immediate))
        assert autd.link.current_stm_segment(0) == Segment.S0
