from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, ControlPoint, FocusSTM, Hz, LoopBehavior, SamplingConfig, Segment, Silencer
from pyautd3.driver.datagram.segment import SwapSegment
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_focus_stm():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        radius = 30.0
        size = 2
        center = np.array([0.0, 0.0, 150.0])
        stm = (
            FocusSTM.from_freq(1.0 * Hz)
            .add_foci_from_iter(
                center + radius * np.array([np.cos(theta), np.sin(theta), 0]) for theta in (2.0 * np.pi * i / size for i in range(size))
            )
            .with_loop_behavior(LoopBehavior.Once)
        )
        autd.send(stm)
        for dev in autd.geometry:
            assert not autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
            assert autd.link.stm_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
            assert autd.link.sound_speed(dev.idx, Segment.S0) == int(dev.sound_speed / 1000.0 * 1024.0)
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 10240000

        stm = FocusSTM.from_freq_nearest(1.0 * Hz).add_focus(center).add_focus(center)
        autd.send(stm)
        for dev in autd.geometry:
            assert not autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
            assert autd.link.stm_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
            assert autd.link.sound_speed(dev.idx, Segment.S0) == int(dev.sound_speed / 1000.0 * 1024.0)
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 10240000

        stm = FocusSTM.from_sampling_config(SamplingConfig.Division(512)).add_focus(center).add_focus(center)
        autd.send(stm)
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 512
        for dev in autd.geometry:
            assert autd.link.stm_cycle(dev.idx, Segment.S0) == 2
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 1)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)


def test_focus_stm_segment():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link.current_stm_segment(0) == Segment.S0

        autd.send(
            FocusSTM.from_sampling_config(SamplingConfig.DivisionRaw(0x12345678)).add_foci_from_iter(
                [ControlPoint(np.zeros(3), EmitIntensity(0x01)), ControlPoint(np.zeros(3), EmitIntensity(0x02))],
            ),
        )
        assert autd.link.current_stm_segment(0) == Segment.S0
        assert autd.link.stm_cycle(0, Segment.S0) == 2
        assert autd.link.stm_freqency_division(0, Segment.S0) == 0x12345678
        for dev in autd.geometry:
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 0)[0] == 0x01)
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 1)[0] == 0x02)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 0)[0] == 0x00)

        autd.send(
            FocusSTM.from_sampling_config(SamplingConfig.DivisionRaw(0x9ABCDEF0))
            .add_foci_from_iter(
                [ControlPoint(np.zeros(3), EmitIntensity(0x03)), ControlPoint(np.zeros(3), EmitIntensity(0x04))],
            )
            .with_segment(Segment.S1, TransitionMode.Immediate),
        )
        assert autd.link.current_stm_segment(0) == Segment.S1
        assert autd.link.stm_cycle(0, Segment.S1) == 2
        assert autd.link.stm_freqency_division(0, Segment.S1) == 0x9ABCDEF0
        for dev in autd.geometry:
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 0)[0] == 0x01)
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 1)[0] == 0x02)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 0)[0] == 0x03)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 1)[0] == 0x04)

        autd.send(
            FocusSTM.from_sampling_config(SamplingConfig.DivisionRaw(0x87654321))
            .add_foci_from_iter(
                [
                    ControlPoint(np.zeros(3), EmitIntensity(0x05)),
                    ControlPoint(np.zeros(3), EmitIntensity(0x06)),
                    ControlPoint(np.zeros(3), EmitIntensity(0x07)),
                ],
            )
            .with_segment(Segment.S0, None),
        )
        assert autd.link.current_stm_segment(0) == Segment.S1
        assert autd.link.stm_cycle(0, Segment.S0) == 3
        assert autd.link.stm_freqency_division(0, Segment.S0) == 0x87654321
        for dev in autd.geometry:
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 0)[0] == 0x05)
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 1)[0] == 0x06)
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 2)[0] == 0x07)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 0)[0] == 0x03)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 1)[0] == 0x04)

        autd.send(SwapSegment.focus_stm(Segment.S0, TransitionMode.Immediate))
        assert autd.link.current_stm_segment(0) == Segment.S0


def test_focus_stm_ctor():
    with pytest.raises(NotImplementedError):
        _ = FocusSTM()
