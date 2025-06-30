from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, FixedCompletionTime, FixedUpdateRate, GainSTM, SamplingConfig, Silencer
from pyautd3.autd_error import AUTDError
from pyautd3.driver.common.freq import Hz
from pyautd3.driver.datagram.stm.foci import FociSTM
from pyautd3.driver.datagram.stm.gain import GainSTMOption
from pyautd3.gain import Null
from pyautd3.modulation import Sine
from pyautd3.modulation.sine import SineOption
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.utils import Duration
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_silencer_from_completion_time():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 10
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 40
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())
            assert autd.link().silencer_strict(dev.idx())

        autd.send(
            Silencer(
                config=FixedCompletionTime(
                    intensity=Duration.from_micros(25 * 2),
                    phase=Duration.from_micros(25 * 3),
                ),
            ),
        )

        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 2
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 3
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())
            assert autd.link().silencer_strict(dev.idx())

        autd.send(
            Silencer(
                config=FixedCompletionTime(
                    intensity=Duration.from_micros(25 * 2),
                    phase=Duration.from_micros(25 * 3),
                    strict=False,
                ),
            ),
        )

        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 2
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 3
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())
            assert not autd.link().silencer_strict(dev.idx())

        autd.send(Silencer())

        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 10
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 40
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())
            assert autd.link().silencer_strict(dev.idx())
            silencer = Silencer()
            assert bool(
                Base().datagram_silencer_fixed_completion_steps_is_default(
                    silencer.config._inner(),  # type: ignore[arg-type]
                ),
            )


def test_silencer_from_update_rate():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 10
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 40
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())

        autd.send(
            Silencer(
                config=FixedUpdateRate(intensity=2, phase=3),
            ),
        )

        for dev in autd.geometry():
            assert autd.link().silencer_update_rate_intensity(dev.idx()) == 2
            assert autd.link().silencer_update_rate_phase(dev.idx()) == 3
            assert not autd.link().silencer_fixed_completion_steps_mode(dev.idx())


def test_silencer_large_steps():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Silencer.disable())
        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 1
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 1
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())
        autd.send(Sine(freq=150 * Hz, option=SineOption(sampling_config=SamplingConfig(1))))

        with pytest.raises(AUTDError) as e:
            autd.send(
                Silencer(
                    config=FixedCompletionTime(
                        intensity=Duration.from_micros(25 * 10),
                        phase=Duration.from_micros(25 * 40),
                    ),
                ),
            )
        assert (
            str(e.value)
            == "Silencer cannot complete phase/intensity interpolation in the specified sampling period. Please lower the sampling frequency or make the completion time of Silencer longer than the sampling period of the AM/STM."  # noqa: E501
        )


def test_silencer_small_freq_div_mod():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 10
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 40
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())

        with pytest.raises(AUTDError) as e:
            autd.send(Sine(freq=150 * Hz, option=SineOption(sampling_config=SamplingConfig(1))))
        assert (
            str(e.value)
            == "Silencer cannot complete phase/intensity interpolation in the specified sampling period. Please lower the sampling frequency or make the completion time of Silencer longer than the sampling period of the AM/STM."  # noqa: E501
        )

        autd.send(
            Silencer(
                config=FixedCompletionTime(
                    intensity=Duration.from_micros(25 * 10),
                    phase=Duration.from_micros(25 * 40),
                    strict=False,
                ),
            ),
        )
        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 10
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 40
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())
        autd.send(Sine(freq=150 * Hz, option=SineOption(sampling_config=SamplingConfig(1))))


def test_silencer_small_freq_div_gain_stm():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 10
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 40
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())

        with pytest.raises(AUTDError) as e:
            autd.send(GainSTM(gains=[Null(), Null()], config=SamplingConfig(1), option=GainSTMOption()))
        assert (
            str(e.value)
            == "Silencer cannot complete phase/intensity interpolation in the specified sampling period. Please lower the sampling frequency or make the completion time of Silencer longer than the sampling period of the AM/STM."  # noqa: E501
        )

        autd.send(
            Silencer(
                config=FixedCompletionTime(
                    intensity=Duration.from_micros(25 * 10),
                    phase=Duration.from_micros(25 * 40),
                    strict=False,
                ),
            ),
        )
        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 10
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 40
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())
        autd.send(GainSTM(gains=[Null(), Null()], config=SamplingConfig(1), option=GainSTMOption()))


def test_silencer_small_freq_div_foci_stm():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 10
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 40
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())

        with pytest.raises(AUTDError) as e:
            autd.send(FociSTM(foci=[np.zeros(3), np.zeros(3)], config=SamplingConfig(1)))
        assert (
            str(e.value)
            == "Silencer cannot complete phase/intensity interpolation in the specified sampling period. Please lower the sampling frequency or make the completion time of Silencer longer than the sampling period of the AM/STM."  # noqa: E501
        )

        autd.send(
            Silencer(
                config=FixedCompletionTime(
                    intensity=Duration.from_micros(25 * 10),
                    phase=Duration.from_micros(25 * 40),
                    strict=False,
                ),
            ),
        )
        for dev in autd.geometry():
            assert autd.link().silencer_completion_steps_intensity(dev.idx()) == 10
            assert autd.link().silencer_completion_steps_phase(dev.idx()) == 40
            assert autd.link().silencer_fixed_completion_steps_mode(dev.idx())

        autd.send(FociSTM(foci=[np.zeros(3), np.zeros(3)], config=SamplingConfig(1)))
