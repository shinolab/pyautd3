from typing import TYPE_CHECKING

import numpy as np
import pytest

from pyautd3 import Controller, Segment
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.gain.holo import EmissionConstraint, Naive, NalgebraBackend, Pa
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_constraint_uniform():
    autd: Controller[Audit]
    with create_controller() as autd:
        backend = NalgebraBackend()
        g = Naive(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30])).with_constraint(
            EmissionConstraint.Uniform(EmitIntensity(0x80)),
        )
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


def test_constraint_normalize():
    autd: Controller[Audit]
    with create_controller() as autd:
        backend = NalgebraBackend()
        g = Naive(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30])).with_constraint(
            EmissionConstraint.Normalize,
        )
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)


def test_constraint_clamp():
    autd: Controller[Audit]
    with create_controller() as autd:
        backend = NalgebraBackend()
        g = Naive(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30])).with_constraint(
            EmissionConstraint.Clamp(EmitIntensity(67), EmitIntensity(85)),
        )
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities >= 67)
            assert np.all(intensities <= 85)
            assert not np.all(phases == 0)


def test_constraint_multiply():
    autd: Controller[Audit]
    with create_controller() as autd:
        backend = NalgebraBackend()
        g = Naive(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30])).with_constraint(
            EmissionConstraint.Multiply(0),
        )
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0)
            assert not np.all(phases == 0)


def test_constraint_ctor():
    with pytest.raises(NotImplementedError):
        _ = EmissionConstraint()
