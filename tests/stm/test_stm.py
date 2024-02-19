from datetime import timedelta
from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import ConfigureSilencer, Controller, FocusSTM, GainSTM, GainSTMMode, SamplingConfiguration, Segment, Uniform
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
        stm = FocusSTM.from_freq(1.0).add_foci_from_iter(
            center + radius * np.array([np.cos(theta), np.sin(theta), 0]) for theta in (2.0 * np.pi * i / size for i in range(size))
        )
        assert await autd.send_async(stm)
        for dev in autd.geometry:
            assert not autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
        assert stm.frequency == 1.0
        assert stm.period == timedelta(microseconds=1000000)
        assert stm.sampling_config.frequency == 2 * 1.0
        assert stm.sampling_config.frequency_division == 10240000
        assert stm.sampling_config.period == timedelta(microseconds=500000)
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
async def test_gain_stm():
    autd: Controller[Audit]
    with await create_controller() as autd:
        assert await autd.send_async(ConfigureSilencer.disable())

        size = 2
        stm = GainSTM.from_freq(1.0).add_gains_from_iter(Uniform(0xFF // (i + 1)) for i in range(size))
        assert await autd.send_async(stm)
        for dev in autd.geometry:
            assert autd.link.is_stm_gain_mode(dev.idx, Segment.S0)
        assert stm.frequency == 1.0
        assert stm.period == timedelta(microseconds=1000000)
        assert stm.sampling_config.frequency == 2 * 1.0
        assert stm.sampling_config.frequency_division == 10240000
        assert stm.sampling_config.period == timedelta(microseconds=500000)
        for dev in autd.geometry:
            assert autd.link.stm_freqency_division(dev.idx, Segment.S0) == 10240000

        stm = GainSTM.from_period(timedelta(microseconds=1000000)).add_gain(Uniform(0xFF)).add_gain(Uniform(0x80))
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
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 1)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0)

        stm = GainSTM.from_sampling_config(SamplingConfiguration.from_frequency_division(512)).add_gain(Uniform(0xFF)).add_gain(Uniform(0x80))
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
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 1)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0)

        stm = (
            GainSTM.from_sampling_config(SamplingConfiguration.from_period(timedelta(microseconds=25)))
            .add_gain(Uniform(0xFF))
            .add_gain(Uniform(0x80))
        )
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
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 1)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0)

        stm = stm.with_mode(GainSTMMode.PhaseFull)
        assert await autd.send_async(stm)
        for dev in autd.geometry:
            assert autd.link.stm_cycle(dev.idx, Segment.S0) == 2
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 1)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)

        stm = stm.with_mode(GainSTMMode.PhaseHalf)
        assert await autd.send_async(stm)
        for dev in autd.geometry:
            assert autd.link.stm_cycle(dev.idx, Segment.S0) == 2
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 1)
            assert np.all(intensities == 0xFF)
            assert np.all(phases == 0)
