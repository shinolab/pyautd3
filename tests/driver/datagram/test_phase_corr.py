from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Phase, PhaseCorrection, Segment
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_phase_corr():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(PhaseCorrection(lambda dev: lambda tr: Phase(dev.idx + tr.idx)))

        for dev in autd.geometry:
            intensities, phases = autd.link.drives_at(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x00)
            for i, phase in enumerate(phases):
                assert phase == dev.idx + i
