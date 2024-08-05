from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, SamplingConfig, Segment
from pyautd3.autd_error import AUTDError
from pyautd3.driver.defined.freq import Hz
from pyautd3.modulation import Square
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_square():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Square(200 * Hz).with_low(32).with_high(85).with_duty(0.1)
        assert m.freq == 200 * Hz
        assert m.low == 32
        assert m.high == 85
        assert m.duty == 0.1
        autd.send(m)

        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [85, 85, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32]
            assert np.array_equal(mod, mod_expect)
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 10

        autd.send(
            Square(150 * Hz).with_sampling_config(SamplingConfig(20)),
        )
        for dev in autd.geometry:
            assert autd.link.modulation_frequency_division(dev.idx, Segment.S0) == 20


def test_square_mode():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Square.nearest(150.0 * Hz)
        assert m.freq == 150.0 * Hz
        autd.send(m)
        for dev in autd.geometry:
            mod = autd.link.modulation(dev.idx, Segment.S0)
            mod_expect = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            assert np.array_equal(mod, mod_expect)

        with pytest.raises(AUTDError):
            autd.send(Square(100.1 * Hz))

        autd.send(Square.nearest(100.1 * Hz))


def test_square_default():
    m = Square(150.0 * Hz)
    assert m.freq == 150.0 * Hz
    assert Base().modulation_square_is_default(m._modulation_ptr())


def test_square_error():
    with pytest.raises(TypeError):
        _ = Square(100 * Hz).with_low(1.0)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        _ = Square(100 * Hz).with_high(1.0)  # type: ignore[arg-type]
