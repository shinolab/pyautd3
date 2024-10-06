from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, LoopBehavior, SamplingConfig, Segment, rad
from pyautd3.autd_error import AUTDError
from pyautd3.driver.defined.freq import Hz
from pyautd3.modulation import Sine
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_sine():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Sine(150 * Hz).with_intensity(0xFF // 2).with_offset(0xFF // 2).with_phase(np.pi / 2 * rad).with_loop_behavior(LoopBehavior.Once)
        assert m.freq == 150 * Hz
        assert m.intensity == 0xFF // 2
        assert m.offset == 0xFF // 2
        assert m.phase == np.pi / 2 * rad
        assert m.loop_behavior == LoopBehavior.Once
        assert m.sampling_config == SamplingConfig(10)
        autd.send(m)

        for dev in autd.geometry:
            assert autd.link.modulation_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            mod_expect = [
                127,
                125,
                120,
                112,
                101,
                88,
                73,
                59,
                44,
                30,
                19,
                9,
                3,
                0,
                1,
                5,
                12,
                22,
                35,
                49,
                64,
                78,
                92,
                105,
                115,
                122,
                126,
                127,
                124,
                118,
                108,
                97,
                83,
                68,
                54,
                39,
                26,
                15,
                7,
                2,
                0,
                2,
                7,
                15,
                26,
                39,
                54,
                68,
                83,
                97,
                108,
                118,
                124,
                127,
                126,
                122,
                115,
                105,
                92,
                78,
                64,
                49,
                35,
                22,
                12,
                5,
                1,
                0,
                3,
                9,
                19,
                30,
                44,
                59,
                73,
                88,
                101,
                112,
                120,
                125,
            ]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10

        m = Sine(150 * Hz).with_sampling_config(SamplingConfig(20))
        autd.send(m)
        assert m.sampling_config == SamplingConfig(20)
        for dev in autd.geometry:
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 20


def test_sine_clamp():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Sine(200 * Hz).with_offset(0).with_clamp(False)  # noqa: FBT003
        assert not m.clamp
        with pytest.raises(AUTDError) as e:
            autd.send(m)
        assert str(e.value) == "Sine modulation value (-39) is out of range [0, 255]"

    with create_controller() as autd:
        m = Sine(200 * Hz).with_offset(0).with_clamp(True)  # noqa: FBT003
        assert m.freq == 200 * Hz
        assert m.intensity == 0xFF
        assert m.offset == 0
        assert m.clamp
        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            mod_expect = [0, 39, 75, 103, 121, 128, 121, 103, 75, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            assert np.array_equal(mod, mod_expect)


def test_sine_mode():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Sine.nearest(150.0 * Hz)
        assert m.freq == 150.0 * Hz
        autd.send(m)
        for dev in autd.geometry:
            mod = autd.link.modulation_buffer(dev.idx, Segment.S0)
            mod_expect = [128, 157, 185, 209, 230, 245, 253, 255, 250, 238, 220, 198, 171, 142, 113, 84, 57, 35, 17, 5, 0, 2, 10, 25, 46, 70, 98]
            assert np.array_equal(mod, mod_expect)

        with pytest.raises(AUTDError):
            autd.send(Sine(100.1 * Hz))

        autd.send(Sine.nearest(100.1 * Hz))


def test_sine_default():
    m = Sine(150.0 * Hz)
    assert m.freq == 150.0 * Hz
    assert Base().modulation_sine_is_default(m._modulation_ptr())


def test_sine_error():
    with pytest.raises(TypeError):
        _ = Sine(100 * Hz).with_intensity(1.0)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        _ = Sine(100 * Hz).with_offset(1.0)  # type: ignore[arg-type]
