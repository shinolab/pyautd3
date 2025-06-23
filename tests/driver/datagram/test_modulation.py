from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment, Static
from pyautd3.driver.datagram.segment import SwapSegment
from pyautd3.driver.datagram.with_loop_behavior import WithLoopBehavior
from pyautd3.driver.datagram.with_segment import WithSegment
from pyautd3.driver.firmware.fpga.loop_behavior import LoopBehavior
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
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
            WithSegment(
                inner=Static(intensity=0x02),
                segment=Segment.S1,
                transition_mode=TransitionMode.Immediate,
            ),
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
                transition_mode=None,
            ),
        )
        assert autd.link().current_mod_segment(0) == Segment.S1
        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S0)
            assert np.all(mod == 0x03)
        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S1)
            assert np.all(mod == 0x02)

        autd.send(SwapSegment.Modulation(Segment.S0, TransitionMode.Immediate))
        assert autd.link().current_mod_segment(0) == Segment.S0


def test_mod_loop_behavior():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(
            WithLoopBehavior(
                inner=Static(intensity=0x02),
                segment=Segment.S1,
                transition_mode=TransitionMode.SyncIdx,
                loop_behavior=LoopBehavior.ONCE,
            ),
        )
        assert autd.link().modulation_loop_behavior(0, Segment.S1) == LoopBehavior.ONCE
