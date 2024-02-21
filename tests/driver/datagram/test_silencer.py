from typing import TYPE_CHECKING

import pytest

from pyautd3 import (
    ConfigureSilencer,
    Controller,
    GainSTM,
    SamplingConfiguration,
)
from pyautd3.autd_error import AUTDError
from pyautd3.gain import Null
from pyautd3.modulation import Sine
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_silencer_fixed_completion_steps():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        await autd.send_async(ConfigureSilencer.fixed_completion_steps(2, 3))

        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 2
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 3
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        await autd.send_async(ConfigureSilencer.disable())

        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 1
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 1
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        await autd.send_async(ConfigureSilencer.default())

        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        assert Base().datagram_silencer_fixed_completion_steps_is_default(ConfigureSilencer.default()._datagram_ptr(0))  # type: ignore [arg-type]


@pytest.mark.asyncio()
async def test_silencer_fixed_update_rate():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        await autd.send_async(ConfigureSilencer.fixed_update_rate(2, 3))

        for dev in autd.geometry:
            assert autd.link.silencer_update_rate_intensity(dev.idx) == 2
            assert autd.link.silencer_update_rate_phase(dev.idx) == 3
            assert not autd.link.silencer_fixed_completion_steps_mode(dev.idx)


@pytest.mark.asyncio()
async def test_silencer_large_steps():
    autd: Controller[Audit]
    with await create_controller() as autd:
        await autd.send_async(ConfigureSilencer.disable())
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 1
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 1
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        assert await autd.send_async(Sine(150).with_sampling_config(SamplingConfiguration.from_frequency_division(512)))

        with pytest.raises(AUTDError) as e:
            await autd.send_async(ConfigureSilencer.fixed_completion_steps(10, 40))
        assert str(e.value) == "Completion steps is too large"


@pytest.mark.asyncio()
async def test_silencer_small_freq_div_mod():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        with pytest.raises(AUTDError) as e:
            await autd.send_async(Sine(150).with_sampling_config(SamplingConfiguration.from_frequency_division(512)))
        assert str(e.value) == "Frequency division is too small"

        await autd.send_async(ConfigureSilencer.fixed_completion_steps(10, 40).with_strict_mode(mode=False))
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        assert await autd.send_async(Sine(150).with_sampling_config(SamplingConfiguration.from_frequency_division(512)))


@pytest.mark.asyncio()
async def test_silencer_small_freq_div_stm():
    autd: Controller[Audit]
    with await create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        with pytest.raises(AUTDError) as e:
            await autd.send_async(GainSTM.from_sampling_config(SamplingConfiguration.from_frequency_division(512)).add_gain(Null()).add_gain(Null()))
        assert str(e.value) == "Frequency division is too small"

        await autd.send_async(ConfigureSilencer.fixed_completion_steps(10, 40).with_strict_mode(mode=False))
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        assert await autd.send_async(
            GainSTM.from_sampling_config(SamplingConfiguration.from_frequency_division(512)).add_gain(Null()).add_gain(Null()),
        )
