import numpy as np
import pytest

from pyautd3 import AUTD3, Controller, Segment
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.gain.holo import LM, EmissionConstraint, NalgebraBackend, Pa
from pyautd3.link.audit import Audit
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as Holo


def test_lm():
    autd: Controller[Audit]
    with Controller[Audit].builder([AUTD3([0.0, 0.0, 0.0])]).open(Audit.builder()) as autd:
        backend = NalgebraBackend()

        g = LM(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30]))
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)

        g = (
            LM(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30]))
            .with_eps1(1e-3)
            .with_eps2(1e-3)
            .with_tau(1e-3)
            .with_kmax(5)
            .with_initial(np.zeros(1))
            .with_constraint(EmissionConstraint.Uniform(EmitIntensity(0x80)))
        )
        assert g.eps1 == 1e-3
        assert g.eps2 == 1e-3
        assert g.tau == 1e-3
        assert g.kmax == 5
        assert np.array_equal(g.initial, np.zeros(1))
        autd.send(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


@pytest.mark.cuda()
def test_lm_cuda():
    from pyautd3.gain.holo.backend_cuda import CUDABackend

    autd: Controller[Audit]
    with Controller[Audit].builder([AUTD3([0.0, 0.0, 0.0])]).open(Audit.builder()) as autd:
        backend = CUDABackend()

        g = LM(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30]))
        autd.send(g)
        for dev in autd.geometry:
            intensities, _ = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)

        g = (
            LM(backend, ((autd.geometry.center + np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30]))
            .with_eps1(1e-3)
            .with_eps2(1e-3)
            .with_tau(1e-3)
            .with_kmax(5)
            .with_initial(np.zeros(1))
            .with_constraint(EmissionConstraint.Uniform(EmitIntensity(0x80)))
        )
        autd.send(g)
        for dev in autd.geometry:
            intensities, _ = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)


def test_gspat_default():
    g = LM(NalgebraBackend(), ((np.array([0, x, 150]), 5e3 * Pa) for x in [-30, 30]))
    assert Holo().gain_lm_is_default(g._gain_ptr(0))  # type: ignore [arg-type]
