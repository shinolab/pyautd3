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
        m = Sine(150 * Hz).with_intensity(0xFF // 2).with_offset(0xFF // 4).with_phase(np.pi / 2 * rad).with_loop_behavior(LoopBehavior.Once)
        assert m.freq == 150 * Hz
        assert m.intensity == 0xFF // 2
        assert m.offset == 0xFF // 4
        assert m.phase == np.pi / 2 * rad
        assert m.loop_behavior == LoopBehavior.Once
        assert m.sampling_config == SamplingConfig(10)
        autd.send(m)

        for dev in autd.geometry:
            assert autd.link.modulation_loop_behavior(dev.idx, Segment.S0) == LoopBehavior.Once
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [
                127,
                125,
                120,
                111,
                100,
                87,
                73,
                58,
                43,
                30,
                18,
                9,
                3,
                0,
                0,
                4,
                12,
                22,
                34,
                48,
                63,
                78,
                92,
                104,
                114,
                122,
                126,
                126,
                123,
                117,
                108,
                96,
                83,
                68,
                53,
                39,
                26,
                15,
                6,
                1,
                0,
                1,
                6,
                15,
                26,
                39,
                53,
                68,
                83,
                96,
                108,
                117,
                123,
                126,
                126,
                122,
                114,
                104,
                92,
                78,
                63,
                48,
                34,
                22,
                12,
                4,
                0,
                0,
                3,
                9,
                18,
                30,
                43,
                58,
                73,
                87,
                100,
                111,
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


def test_sine_mode():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Sine.nearest(150.0 * Hz)
        assert m.freq == 150.0 * Hz
        autd.send(m)
        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [127, 156, 184, 209, 229, 244, 253, 254, 249, 237, 220, 197, 171, 142, 112, 83, 57, 34, 17, 5, 0, 1, 10, 25, 45, 70, 98]
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
