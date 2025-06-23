from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, Hz, Intensity, Phase, Segment
from pyautd3.autd_error import InvalidDatagramTypeError
from pyautd3.driver.datagram.group import Group
from pyautd3.driver.geometry.device import Device
from pyautd3.gain import Uniform
from pyautd3.gain.null import Null
from pyautd3.modulation.sine import Sine, SineOption
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_group():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(
            Group(
                key_map=lambda dev: dev.idx(),
                data_map={1: Null(), 0: (Sine(freq=150 * Hz, option=SineOption()), Uniform(intensity=Intensity(0xFF), phase=Phase(0)))},
            ),
        )

        mod = autd.link().modulation_buffer(0, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link().drives_at(0, Segment.S0, 0)
        assert np.all(intensities == 0xFF)
        assert np.all(phases == 0)

        mod = autd.link().modulation_buffer(1, Segment.S0)
        intensities, phases = autd.link().drives_at(1, Segment.S0, 0)
        assert np.all(intensities == 0)

        with pytest.raises(InvalidDatagramTypeError):
            autd.send(Group(lambda dev: dev.idx(), {0: 0}))  # type: ignore[dict-item]


def test_group_check_only_for_enabled():
    autd: Controller[Audit]
    with create_controller() as autd:

        def key_map(dev: Device) -> int | None:
            if dev.idx() == 0:
                return None
            return 0

        autd.send(
            Group(
                key_map,
                {0: (Sine(freq=150 * Hz, option=SineOption()), Uniform(intensity=Intensity(0x80), phase=Phase(0x90)))},
            ),
        )

        mod = autd.link().modulation_buffer(0, Segment.S0)
        intensities, phases = autd.link().drives_at(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        mod = autd.link().modulation_buffer(1, Segment.S0)
        assert len(mod) == 80
        intensities, phases = autd.link().drives_at(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 0x90)
