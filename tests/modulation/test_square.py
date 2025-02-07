from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, SamplingConfig, Segment
from pyautd3.autd_error import AUTDError
from pyautd3.driver.defined.freq import Hz
from pyautd3.modulation import Square
from pyautd3.modulation.square import SquareOption
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_square():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Square(
            freq=200 * Hz,
            option=SquareOption(
                low=32,
                high=85,
                duty=0.1,
            ),
        )
        autd.send(m)

        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S0)
            mod_expect = [85, 85, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32]
            assert np.array_equal(mod, mod_expect)
            assert autd.link().modulation_frequency_division(dev.idx(), Segment.S0) == 10

        autd.send(Square(freq=150 * Hz, option=SquareOption(sampling_config=SamplingConfig(20))))
        for dev in autd.geometry():
            assert autd.link().modulation_frequency_division(dev.idx(), Segment.S0) == 20


def test_square_nearest():
    autd: Controller[Audit]
    with create_controller() as autd:
        m = Square(freq=150.0 * Hz, option=SquareOption()).into_nearest()
        autd.send(m)
        for dev in autd.geometry():
            mod = autd.link().modulation_buffer(dev.idx(), Segment.S0)
            mod_expect = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            assert np.array_equal(mod, mod_expect)

        with pytest.raises(AUTDError):
            autd.send(Square(freq=100.1 * Hz, option=SquareOption()))

        autd.send(Square(freq=100.1 * Hz, option=SquareOption()).into_nearest())

        with pytest.raises(TypeError):
            _ = Square(freq=100 * Hz, option=SquareOption()).into_nearest()


def test_square_default():
    assert Base().modulation_square_is_default(SquareOption()._inner())
