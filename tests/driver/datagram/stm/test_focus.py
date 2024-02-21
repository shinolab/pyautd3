from datetime import timedelta
from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import ChangeFocusSTMSegment, ConfigureSilencer, Controller, ControlPoint, FocusSTM, LoopBehavior, SamplingConfiguration, Segment
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_focus_stm():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert await autd.send_async(ConfigureSilencer.disable())

        radius = 30.0
        size = 2
        center = np.array([0.0, 0.0, 150.0])
        stm = (
            FocusSTM.from_freq(1.0)
            .add_foci_from_iter(
                center + radius * np.array([np.cos(theta), np.sin(theta), 0]) for theta in (2.0 * np.pi * i / size for i in range(size))
            )
            .with_loop_behavior(LoopBehavior.once())
        )
        assert await autd.send_async(stm)
        for dev in autd.geometry:
            assert not autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
            assert autd.link.stm_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.once()
            assert autd.link.sound_speed(dev.idx, Segment.S0) == int(dev.sound_speed / 1000.0 * 1024.0)
        assert stm.frequency == 1.0
        assert stm.period == timedelta(microseconds=1000000)
        assert stm.sampling_config.frequency == 2 * 1.0
        assert stm.sampling_config.frequency_division == 10240000
        assert stm.sampling_config.period == timedelta(microseconds=500000)
        assert stm.loop_behavior == LoopBehavior.once()
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 10240000

        stm = FocusSTM.from_period(timedelta(microseconds=1000000)).add_focus(center).add_focus(center)
        assert await autd.send_async(stm)
        assert stm.frequency == 1
        assert stm.period == timedelta(microseconds=1000000)
        assert stm.sampling_config.frequency == 2 * 1.0
        assert stm.sampling_config.frequency_division == 10240000
        assert stm.sampling_config.period == timedelta(microseconds=500000)
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 10240000
        for dev in autd.geometry:
            assert autd.link.stm_cycle(dev.idx, Segment.S0) == 2
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 1)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)

        stm = FocusSTM.from_sampling_config(SamplingConfiguration.from_frequency_division(512)).add_focus(center).add_focus(center)
        assert await autd.send_async(stm)
        assert stm.frequency == 20000.0
        assert stm.sampling_config.frequency == 2 * 20000.0
        assert stm.sampling_config.frequency_division == 512
        assert stm.sampling_config.period == timedelta(microseconds=25)
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

        stm = FocusSTM.from_sampling_config(SamplingConfiguration.from_period(timedelta(microseconds=25))).add_focus(center).add_focus(center)
        assert await autd.send_async(stm)
        assert stm.frequency == 20000.0
        assert stm.sampling_config.frequency == 2 * 20000.0
        assert stm.sampling_config.frequency_division == 512
        assert stm.sampling_config.period == timedelta(microseconds=25)
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


@pytest.mark.asyncio()
async def test_focus_stm_segment():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert autd.link.current_stm_segment(0) == Segment.S0

        assert await autd.send_async(
            FocusSTM.from_sampling_config(SamplingConfiguration.from_frequency_division(0x12345678)).add_foci_from_iter(
                [ControlPoint(np.zeros(3), 0x01), ControlPoint(np.zeros(3), 0x02)],
            ),
        )
        assert autd.link.current_stm_segment(0) == Segment.S0
        assert autd.link.stm_cycle(0, Segment.S0) == 2
        assert autd.link.stm_freqency_division(0, Segment.S0) == 0x12345678
        for dev in autd.geometry:
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 0)[0] == 0x01)
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 1)[0] == 0x02)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 0)[0] == 0x00)

        assert await autd.send_async(
            FocusSTM.from_sampling_config(SamplingConfiguration.from_frequency_division(0x9ABCDEF0))
            .add_foci_from_iter(
                [ControlPoint(np.zeros(3), 0x03), ControlPoint(np.zeros(3), 0x04)],
            )
            .with_segment(Segment.S1, update_segment=True),
        )
        assert autd.link.current_stm_segment(0) == Segment.S1
        assert autd.link.stm_cycle(0, Segment.S1) == 2
        assert autd.link.stm_freqency_division(0, Segment.S1) == 0x9ABCDEF0
        for dev in autd.geometry:
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 0)[0] == 0x01)
            assert np.all(autd.link.drives(dev.idx, Segment.S0, 1)[0] == 0x02)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 0)[0] == 0x03)
            assert np.all(autd.link.drives(dev.idx, Segment.S1, 1)[0] == 0x04)

        assert await autd.send_async(
            FocusSTM.from_sampling_config(SamplingConfiguration.from_frequency_division(0x87654321))
            .add_foci_from_iter(
                [ControlPoint(np.zeros(3), 0x05), ControlPoint(np.zeros(3), 0x06), ControlPoint(np.zeros(3), 0x07)],
            )
            .with_segment(Segment.S0, update_segment=False),
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

        assert await autd.send_async(ChangeFocusSTMSegment(Segment.S0))
        assert autd.link.current_stm_segment(0) == Segment.S0
