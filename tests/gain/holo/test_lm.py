import numpy as np
import pytest

from pyautd3 import AUTD3, Controller, Segment
from pyautd3.gain.holo import LM, EmissionConstraint, NalgebraBackend, pascal
from pyautd3.link.audit import Audit
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as Holo


@pytest.mark.asyncio()
async def test_lm():
    autd: Controller[Audit]
    with await Controller[Audit].builder().add_device(AUTD3([0.0, 0.0, 0.0])).open_async(Audit.builder()) as autd:
        backend = NalgebraBackend()

        g = (
            LM(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
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
            .with_constraint(EmissionConstraint.Uniform(0x80))
        )
        assert g.eps1 == 1e-3
        assert g.eps2 == 1e-3
        assert g.tau == 1e-3
        assert g.kmax == 5
        assert np.array_equal(g.initial, np.zeros(1))
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


@pytest.mark.cuda()
@pytest.mark.asyncio()
async def test_lm_cuda():
    from pyautd3.gain.holo.backend_cuda import CUDABackend

    autd: Controller[Audit]
    with await Controller[Audit].builder().add_device(AUTD3([0.0, 0.0, 0.0])).open_async(Audit.builder()) as autd:
        backend = CUDABackend()

        g = (
            LM(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
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
            .with_constraint(EmissionConstraint.Uniform(0x80))
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


def test_gspat_default():
    g = LM(NalgebraBackend())
    assert Holo().gain_lm_is_default(g._gain_ptr(0))  # type: ignore [arg-type]
