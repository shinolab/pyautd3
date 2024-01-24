import numpy as np
import pytest

from pyautd3 import AUTD3, Controller
from pyautd3.gain.holo import LM, EmissionConstraint, NalgebraBackend, pascal
from pyautd3.link.audit import Audit
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as Holo


@pytest.mark.asyncio()
async def test_lm():
    with await Controller[Audit].builder().add_device(AUTD3([0.0, 0.0, 0.0])).open_with_async(Audit.builder()) as autd:
        backend = NalgebraBackend()

        g = (
            LM(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)

        g = (
            LM(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
            .with_eps1(1e-3)
            .with_eps2(1e-3)
            .with_tau(1e-3)
            .with_kmax(5)
            .with_initial(np.zeros(1))
            .with_constraint(EmissionConstraint.uniform(0x80))
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


@pytest.mark.cuda()
@pytest.mark.asyncio()
async def test_lm_cuda():
    from pyautd3.gain.holo.backend_cuda import CUDABackend

    with await Controller[Audit].builder().add_device(AUTD3([0.0, 0.0, 0.0])).open_with_async(Audit.builder()) as autd:
        backend = CUDABackend()

        g = (
            LM(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)

        g = (
            LM(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
            .with_eps1(1e-3)
            .with_eps2(1e-3)
            .with_tau(1e-3)
            .with_kmax(5)
            .with_initial(np.zeros(1))
            .with_constraint(EmissionConstraint.uniform(0x80))
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


def test_gspat_default():
    g = LM(NalgebraBackend())
    assert g.eps1() == Holo().gain_holo_lm_default_eps_1()
    assert g.eps2() == Holo().gain_holo_lm_default_eps_2()
    assert g.tau() == Holo().gain_holo_lm_default_tau()
    assert g.kmax() == Holo().gain_holo_lm_default_k_max()
    assert g.initial() == []
    assert Holo().gain_holo_constraint_eq(g.constraint()._constraint_ptr(), Holo().gain_holo_lm_default_constraint())
