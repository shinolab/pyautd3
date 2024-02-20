import numpy as np
import pytest

from pyautd3 import AUTD3, Controller, Segment
from pyautd3.gain.holo import SDP, EmissionConstraint, NalgebraBackend, pascal
from pyautd3.link.audit import Audit
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as Holo


@pytest.mark.asyncio()
async def test_sdp():
    autd: Controller[Audit]
    with await Controller[Audit].builder().add_device(AUTD3([0.0, 0.0, 0.0])).open_async(Audit.builder()) as autd:
        backend = NalgebraBackend()

        g = (
            SDP(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)

        g = (
            SDP(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
            .with_alpha(1e-3)
            .with_lambda(0.9)
            .with_repeat(10)
            .with_constraint(EmissionConstraint.uniform(0x80))
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


@pytest.mark.cuda()
@pytest.mark.asyncio()
async def test_sdp_cuda():
    from pyautd3.gain.holo.backend_cuda import CUDABackend

    autd: Controller[Audit]
    with await Controller[Audit].builder().add_device(AUTD3([0.0, 0.0, 0.0])).open_async(Audit.builder()) as autd:
        backend = CUDABackend()

        g = (
            SDP(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert not np.all(intensities == 0)
            assert not np.all(phases == 0)

        g = (
            SDP(backend)
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
            .with_alpha(1e-3)
            .with_lambda(0.9)
            .with_repeat(10)
            .with_constraint(EmissionConstraint.uniform(0x80))
        )
        assert g.alpha() == 1e-3
        assert g.lambda_() == 0.9
        assert g.repeat() == 10
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


def test_sdp_default():
    g = SDP(NalgebraBackend())
    assert Holo().gain_sdp_is_default(g._gain_ptr(0))  # type: ignore [arg-type]
