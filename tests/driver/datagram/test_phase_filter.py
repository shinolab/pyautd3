from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import (
    Controller,
    Phase,
    PhaseFilter,
)
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_phase_filter():
    autd: Controller[Audit]
    with create_controller() as autd:
        for dev in autd.geometry:
            assert np.all(autd.link.phase_filter(dev.idx) == 0x00)

        autd.send(PhaseFilter.additive(lambda dev: lambda tr: Phase((dev.idx + tr.idx) % 256)))

        for dev in autd.geometry:
            phase_filter = autd.link.phase_filter(dev.idx)
            for tr in dev:
                assert phase_filter[tr.idx] == (dev.idx + tr.idx) % 256
