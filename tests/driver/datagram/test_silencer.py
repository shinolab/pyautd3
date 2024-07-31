from datetime import timedelta
from typing import TYPE_CHECKING

import pytest

from pyautd3 import (
    Controller,
    GainSTM,
    SamplingConfig,
    Silencer,
)
from pyautd3.autd_error import AUTDError
from pyautd3.driver.defined.freq import Hz
from pyautd3.gain import Null
from pyautd3.modulation import Sine
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_silencer_from_completion_time():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)
            assert autd.link.silencer_strict_mode(dev.idx)

        autd.send(Silencer.from_completion_time(timedelta(microseconds=25 * 2), timedelta(microseconds=25 * 3)))

        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 2
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 3
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)
            assert autd.link.silencer_strict_mode(dev.idx)

        autd.send(Silencer.from_completion_time(timedelta(microseconds=25 * 2), timedelta(microseconds=25 * 3)).with_strict_mode(mode=False))

        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 2
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 3
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)
            assert not autd.link.silencer_strict_mode(dev.idx)


def test_silencer_from_update_rate():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        autd.send(Silencer.from_update_rate(2, 3))

        for dev in autd.geometry:
            assert autd.link.silencer_update_rate_intensity(dev.idx) == 2
            assert autd.link.silencer_update_rate_phase(dev.idx) == 3
            assert not autd.link.silencer_fixed_completion_steps_mode(dev.idx)


def test_silencer_large_steps():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 1
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 1
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        autd.send(Sine(150 * Hz).with_sampling_config(SamplingConfig(1)))

        with pytest.raises(AUTDError) as e:
            autd.send(Silencer.from_completion_time(timedelta(microseconds=25 * 10), timedelta(microseconds=25 * 40)))
        assert (
            str(e.value)
            == "Silencer cannot complete phase/intensity completion in the specified sampling period. Please lower the sampling frequency or make the completion time of Silencer longer than the sampling period."  # noqa: E501
        )


def test_silencer_small_freq_div_mod():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        with pytest.raises(AUTDError) as e:
            autd.send(Sine(150 * Hz).with_sampling_config(SamplingConfig(1)))
        assert (
            str(e.value)
            == "Silencer cannot complete phase/intensity completion in the specified sampling period. Please lower the sampling frequency or make the completion time of Silencer longer than the sampling period."  # noqa: E501
        )

        autd.send(Silencer.from_completion_time(timedelta(microseconds=25 * 10), timedelta(microseconds=25 * 40)).with_strict_mode(mode=False))
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        autd.send(Sine(150 * Hz).with_sampling_config(SamplingConfig(1)))


def test_silencer_small_freq_div_stm():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        with pytest.raises(AUTDError) as e:
            autd.send(GainSTM(SamplingConfig(1), [Null(), Null()]))
        assert (
            str(e.value)
            == "Silencer cannot complete phase/intensity completion in the specified sampling period. Please lower the sampling frequency or make the completion time of Silencer longer than the sampling period."  # noqa: E501
        )

        autd.send(Silencer.from_completion_time(timedelta(microseconds=25 * 10), timedelta(microseconds=25 * 40)).with_strict_mode(mode=False))
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        autd.send(
            GainSTM(SamplingConfig(1), [Null(), Null()]),
        )
