from datetime import timedelta
from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, GainSTM, GainSTMMode, Hz, LoopBehavior, SamplingConfig, Segment, Silencer, Uniform
from pyautd3.driver.datagram.segment import SwapSegment
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_gain_stm():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())

        size = 2
        stm = GainSTM(1.0 * Hz, (Uniform(EmitIntensity(0xFF // (i + 1))) for i in range(size))).with_loop_behavior(LoopBehavior.Once)
        assert stm.freq == (1.0 * Hz)
        assert stm.period == timedelta(seconds=1.0)
        assert stm.sampling_config == SamplingConfig(20000)
        autd.send(stm)
        for dev in autd.geometry:
            assert autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
            assert autd.link.stm_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
        assert stm.mode == GainSTMMode.PhaseIntensityFull
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 20000

        stm = GainSTM.nearest(1.0 * Hz, [Uniform(EmitIntensity(0xFF)), Uniform(EmitIntensity(0x80))])
        autd.send(stm)
        for dev in autd.geometry:
            assert autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
            assert autd.link.stm_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
        assert stm.mode == GainSTMMode.PhaseIntensityFull
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 20000

        stm = GainSTM(timedelta(seconds=1.0), [Uniform(EmitIntensity(0xFF)), Uniform(EmitIntensity(0x80))])
        autd.send(stm)
        for dev in autd.geometry:
            assert autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
            assert autd.link.stm_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
        assert stm.mode == GainSTMMode.PhaseIntensityFull
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 20000

        stm = GainSTM.nearest(timedelta(seconds=1.0), [Uniform(EmitIntensity(0xFF)), Uniform(EmitIntensity(0x80))])
        autd.send(stm)
        for dev in autd.geometry:
            assert autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
            assert autd.link.stm_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
        assert stm.mode == GainSTMMode.PhaseIntensityFull
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 20000

        stm = GainSTM(SamplingConfig(1), [Uniform(EmitIntensity(0xFF)), Uniform(EmitIntensity(0x80))])
        autd.send(stm)
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 1
        for dev in autd.geometry:
            assert autd.link.stm_cycle(dev.idx, Segment.S0) == 2
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 1)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0)

        stm = stm.with_mode(GainSTMMode.PhaseFull)
        assert stm.mode == GainSTMMode.PhaseFull
        autd.send(stm)
        for dev in autd.geometry:
            assert autd.link.stm_cycle(dev.idx, Segment.S0) == 2
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 1)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)

        stm = stm.with_mode(GainSTMMode.PhaseHalf)
        assert stm.mode == GainSTMMode.PhaseHalf
        autd.send(stm)
        for dev in autd.geometry:
            assert autd.link.stm_cycle(dev.idx, Segment.S0) == 2
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 1)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)


def test_gain_stm_segment():
    autd: Controller[Audit]
    with create_controller() as autd:
        assert autd.link.current_stm_segment(0) == Segment.S0

        autd.send(
            GainSTM(
                SamplingConfig(0x1234),
                [Uniform(EmitIntensity(0x01)), Uniform(EmitIntensity(0x02))],
            ),
        )
        assert autd.link.current_stm_segment(0) == Segment.S0
        assert autd.link.stm_cycle(0, Segment.S0) == 2
        assert autd.link.stm_freqency_division(0, Segment.S0) == 0x1234
        for dev in autd.geometry:
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 0)[0] == 0x01)
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 1)[0] == 0x02)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 0)[0] == 0x00)

        autd.send(
            GainSTM(
                SamplingConfig(0x9ABC),
                [Uniform(EmitIntensity(0x03)), Uniform(EmitIntensity(0x04))],
            ).with_segment(Segment.S1, TransitionMode.Immediate),
        )
        assert autd.link.current_stm_segment(0) == Segment.S1
        assert autd.link.stm_cycle(0, Segment.S1) == 2
        assert autd.link.stm_freqency_division(0, Segment.S1) == 0x9ABC
        for dev in autd.geometry:
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 0)[0] == 0x01)
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 1)[0] == 0x02)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 0)[0] == 0x03)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 1)[0] == 0x04)

        autd.send(
            GainSTM(
                SamplingConfig(0x4321),
                [Uniform(EmitIntensity(0x05)), Uniform(EmitIntensity(0x06)), Uniform(EmitIntensity(0x07))],
            ).with_segment(Segment.S0, None),
        )
        assert autd.link.current_stm_segment(0) == Segment.S1
        assert autd.link.stm_cycle(0, Segment.S0) == 3
        assert autd.link.stm_freqency_division(0, Segment.S0) == 0x4321
        for dev in autd.geometry:
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 0)[0] == 0x05)
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 1)[0] == 0x06)
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 2)[0] == 0x07)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 0)[0] == 0x03)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 1)[0] == 0x04)

        autd.send(SwapSegment.GainSTM(Segment.S0, TransitionMode.Immediate))
        assert autd.link.current_stm_segment(0) == Segment.S0
