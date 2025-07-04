from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, Device, Segment, Transducer
from pyautd3.autd_error import AUTDError
from pyautd3.driver.firmware.fpga.emit_intensity import Intensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.gain import Group, Null, Uniform
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_group():
    autd: Controller[Audit]
    with create_controller() as autd:
        cx = autd.center()[0]

        g = Group(
            key_map=lambda _: lambda tr: "uniform" if tr.position()[0] < cx else "null",
            gain_map={"uniform": Uniform(intensity=Intensity(0x80), phase=Phase(0x90)), "null": Null()},
        )
        autd.send(g)
        for dev in autd.geometry():
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            for tr in dev:
                if tr.position()[0] < cx:
                    assert np.all(intensities[tr.idx()] == 0x80)
                    assert np.all(phases[tr.idx()] == 0x90)
                else:
                    assert np.all(intensities[tr.idx()] == 0)
                    assert np.all(phases[tr.idx()] == 0)

        autd.send(
            Group(
                key_map=lambda _: lambda tr: "uniform" if tr.position()[0] < cx else None,
                gain_map={"uniform": Uniform(intensity=Intensity(0x80), phase=Phase(0x90))},
            ),
        )
        for dev in autd.geometry():
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            for tr in dev:
                if tr.position()[0] < cx:
                    assert np.all(intensities[tr.idx()] == 0x80)
                    assert np.all(phases[tr.idx()] == 0x90)
                else:
                    assert np.all(intensities[tr.idx()] == 0)
                    assert np.all(phases[tr.idx()] == 0)


def test_group_unknown_key():
    autd: Controller[Audit]
    with create_controller() as autd, pytest.raises(AUTDError, match="Unknown group key"):
        autd.send(Group(lambda _: lambda _tr: "null", {"uniform": Uniform(intensity=Intensity(0x80), phase=Phase(0x90)), "null": Null()}))


def test_group_check_only_for_enabled():
    autd: Controller[Audit]
    with create_controller() as autd:

        def key_map(dev: Device) -> Callable[[Transducer], int | None]:
            if dev.idx() == 0:
                return lambda _: None
            return lambda _: 0

        autd.send(Group(key_map, {0: Uniform(intensity=Intensity(0x80), phase=Phase(0x90))}))

        intensities, phases = autd.link().drives_at(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        intensities, phases = autd.link().drives_at(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 0x90)
