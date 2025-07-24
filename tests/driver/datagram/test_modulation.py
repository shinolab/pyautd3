from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment, Static, transition_mode
from pyautd3.driver.datagram.segment import SwapSegmentModulation
from pyautd3.driver.datagram.with_finite_loop import WithFiniteLoop
from pyautd3.driver.datagram.with_segment import WithSegment
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_mod_segment():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link().current_mod_segment(0) == Segment.S0

        autd.send(Static(intensity=0x01))
        assert autd.link().current_mod_segment(0) == Segment.S0
        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S0)
            assert np.all(mod == 0x01)
        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S1)
            assert np.all(mod == 0xFF)

        autd.send(
            WithSegment(inner=Static(intensity=0x02), segment=Segment.S1, transition_mode=transition_mode.Immediate()),
        )
        assert autd.link().current_mod_segment(0) == Segment.S1
        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S0)
            assert np.all(mod == 0x01)
        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S1)
            assert np.all(mod == 0x02)

        autd.send(
            WithSegment(
                inner=Static(intensity=0x03),
                segment=Segment.S0,
                transition_mode=transition_mode.Later(),
            ),
        )
        assert autd.link().current_mod_segment(0) == Segment.S1
        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S0)
            assert np.all(mod == 0x03)
        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S1)
            assert np.all(mod == 0x02)

        autd.send(SwapSegmentModulation(Segment.S0, transition_mode.Immediate()))
        assert autd.link().current_mod_segment(0) == Segment.S0


def test_mod_loop_behavior():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(
            WithFiniteLoop(
                inner=Static(intensity=0x02),
                segment=Segment.S1,
                transition_mode=transition_mode.SyncIdx(),
                loop_count=1,
            ),
        )
        assert autd.link().modulation_loop_count(0, Segment.S1) == 0
