import numpy as np
import pytest

from pyautd3 import AUTD3, Controller, Segment
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.gain.holo import GSPAT, EmissionConstraint, NalgebraBackend, Pa
from pyautd3.link.audit import Audit
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as Holo


def test_gspat():
    autd: Controller[Audit]
    with Controller[Audit].builder([AUTD3([0.0, 0.0, 0.0])]).open(Audit.builder()) as autd:
        backend = NalgebraBackend()
        g = GSPAT(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30]))
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)

        g = (
            GSPAT(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30]))
            .with_repeat(50)
            .with_constraint(EmissionConstraint.Uniform(EmitIntensity(0x80)))
        )
        assert g.repeat == 50
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


@pytest.mark.cuda()
def test_gspat_cuda():
    from pyautd3.gain.holo.backend_cuda import CUDABackend

    autd: Controller[Audit]
    with Controller[Audit].builder([AUTD3([0.0, 0.0, 0.0])]).open(Audit.builder()) as autd:
        backend = CUDABackend()
        g = GSPAT(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30]))
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)

        g = (
            GSPAT(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30]))
            .with_repeat(50)
            .with_constraint(EmissionConstraint.Uniform(EmitIntensity(0x80)))
        )
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


def test_gspat_default():
    g = GSPAT(NalgebraBackend(), ((np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30]))
    assert Holo().gain_gspat_is_default(g._gain_ptr(0))  # type: ignore [arg-type]
