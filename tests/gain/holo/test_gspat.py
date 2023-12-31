"""
File: test_gspat.py
Project: holo
Created Date: 17/10/2023
Author: Shun Suzuki
-----
Last Modified: 11/12/2023
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2023 Shun Suzuki. All rights reserved.

"""


import numpy as np
import pytest

from pyautd3 import AUTD3, Controller
from pyautd3.gain.holo import GSPAT, EmissionConstraint, NalgebraBackend, pascal
from pyautd3.link.audit import Audit


@pytest.mark.asyncio()
async def test_gspat():
    autd = await Controller[Audit].builder().add_device(AUTD3([0.0, 0.0, 0.0])).open_with_async(Audit.builder())

    backend = NalgebraBackend()
    g = (
        GSPAT(backend)
        .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
        .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
    )
    assert await autd.send_async(g)
    for dev in autd.geometry:
        intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
        assert not np.all(intensities == 0)
        assert not np.all(phases == 0)

    g = (
        GSPAT(backend)
        .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
        .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
        .with_repeat(100)
        .with_constraint(EmissionConstraint.uniform(0x80))
    )
    assert await autd.send_async(g)
    for dev in autd.geometry:
        intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
        assert np.all(intensities == 0x80)
        assert not np.all(phases == 0)


@pytest.mark.cuda()
@pytest.mark.asyncio()
async def test_gspat_cuda():
    from pyautd3.gain.holo.backend_cuda import CUDABackend

    autd = await Controller[Audit].builder().add_device(AUTD3([0.0, 0.0, 0.0])).open_with_async(Audit.builder())

    backend = CUDABackend()
    g = (
        GSPAT(backend)
        .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
        .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
    )
    assert await autd.send_async(g)
    for dev in autd.geometry:
        intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
        assert not np.all(intensities == 0)
        assert not np.all(phases == 0)

    g = (
        GSPAT(backend)
        .add_focus(autd.geometry.center + np.array([30, 0, 150]), 5e3 * pascal)
        .add_foci_from_iter((autd.geometry.center + np.array([0, x, 150]), 5e3 * pascal) for x in [-30])
        .with_repeat(100)
        .with_constraint(EmissionConstraint.uniform(0x80))
    )
    assert await autd.send_async(g)
    for dev in autd.geometry:
        intensities, phases = autd.link.intensities_and_phases(dev.idx, 0)
        assert np.all(intensities == 0x80)
        assert not np.all(phases == 0)
