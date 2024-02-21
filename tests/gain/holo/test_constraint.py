from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, Segment
from pyautd3.gain.holo import EmissionConstraint, Naive, NalgebraBackend, pascal
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_constraint():
    autd: Controller[Audit]
    with await create_controller() as autd:
        backend = NalgebraBackend()
        g = (
            Naive(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_focus(autd.geometry.center + np.array([-30, 0, 150]), 5e3 * pascal)
            .with_constraint(EmissionConstraint.Uniform(0x80))
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)

        g = (
            Naive(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_focus(autd.geometry.center + np.array([-30, 0, 150]), 5e3 * pascal)
            .with_constraint(EmissionConstraint.Normalize())
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)

        g = (
            Naive(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_focus(autd.geometry.center + np.array([-30, 0, 150]), 5e3 * pascal)
            .with_constraint(EmissionConstraint.Clamp(67, 85))
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities >= 67)
            assert np.all(intensities <= 85)
            assert not np.all(phases == 0)

        g = (
            Naive(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_focus(autd.geometry.center + np.array([-30, 0, 150]), 5e3 * pascal)
            .with_constraint(EmissionConstraint.DontCare())
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)


def test_constraint_ctor():
    with pytest.raises(NotImplementedError):
        _ = EmissionConstraint()


def test_constraint_eq():
    assert EmissionConstraint.Uniform(0x80) != 0x80
