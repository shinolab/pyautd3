import numpy as np
import pytest

from pyautd3 import AUTD3, Controller, Segment
from pyautd3.gain.holo import EmissionConstraint, Greedy, pascal
from pyautd3.link.audit import Audit
from pyautd3.native_methods.autd3capi_gain_holo import NativeMethods as Holo


@pytest.mark.asyncio()
async def test_greedy():
    autd: Controller[Audit]
    with await Controller[Audit].builder().add_device(AUTD3([0.0, 0.0, 0.0])).open_async(Audit.builder()) as autd:
        g = (
            Greedy()
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
        )
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0xFF)
            assert not np.all(phases == 0)

        g = (
            Greedy()
            .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
            .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
            .with_phase_div(8)
            .with_constraint(EmissionConstraint.Uniform(0x80))
        )
        assert g.constraint() == EmissionConstraint.Uniform(0x80)
        assert g.phase_div() == 8
        assert await autd.send_async(g)
        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert not np.all(phases == 0)


def test_greedy_default():
    g = Greedy()
    assert Holo().gain_greedy_is_default(g._gain_ptr(0))  # type: ignore [arg-type]
