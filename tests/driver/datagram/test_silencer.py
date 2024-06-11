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
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_silencer_fixed_completion_steps():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        autd.send(Silencer.fixed_completion_steps(2, 3))

        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 2
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 3
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        autd.send(Silencer.disable())

        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 1
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 1
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        autd.send(Silencer.default())

        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        assert Base().datagram_silencer_fixed_completion_steps_is_default(Silencer.default()._datagram_ptr(0))  # type: ignore [arg-type]


def test_silencer_fixed_update_rate():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        autd.send(Silencer.fixed_update_rate(2, 3))

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

        autd.send(Sine(150 * Hz).with_sampling_config(SamplingConfig.Division(512)))

        with pytest.raises(AUTDError) as e:
            autd.send(Silencer.fixed_completion_steps(10, 40))
        assert str(e.value) == "Sampling frequency division is too small or silencer completion steps is too large"


def test_silencer_small_freq_div_mod():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        with pytest.raises(AUTDError) as e:
            autd.send(Sine(150 * Hz).with_sampling_config(SamplingConfig.Division(512)))
        assert str(e.value) == "Sampling frequency division is too small or silencer completion steps is too large"

        autd.send(Silencer.fixed_completion_steps(10, 40).with_strict_mode(mode=False))
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        autd.send(Sine(150 * Hz).with_sampling_config(SamplingConfig.Division(512)))


def test_silencer_small_freq_div_stm():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        with pytest.raises(AUTDError) as e:
            autd.send(GainSTM.from_sampling_config(SamplingConfig.Division(512), [Null(), Null()]))
        assert str(e.value) == "Sampling frequency division is too small or silencer completion steps is too large"

        autd.send(Silencer.fixed_completion_steps(10, 40).with_strict_mode(mode=False))
        for dev in autd.geometry:
            assert autd.link.silencer_completion_steps_intensity(dev.idx) == 10
            assert autd.link.silencer_completion_steps_phase(dev.idx) == 40
            assert autd.link.silencer_fixed_completion_steps_mode(dev.idx)

        autd.send(
            GainSTM.from_sampling_config(SamplingConfig.Division(512), [Null(), Null()]),
        )
