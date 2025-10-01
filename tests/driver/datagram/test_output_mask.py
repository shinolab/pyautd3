from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Intensity, OutputMask, Phase, Segment, Uniform, WithSegment, transition_mode
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_output_mask():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.send(Uniform(intensity=Intensity(0x80), phase=Phase(0x81)))

        for dev in autd.geometry():
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x81)

        autd.send(OutputMask(lambda _dev: lambda _tr: False))

        for dev in autd.geometry():
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S0, 0)
            assert np.all(intensities == 0x00)
            assert np.all(phases == 0x81)

        autd.send(
            WithSegment(
                inner=Uniform(intensity=Intensity(0x80), phase=Phase(0x81)),
                segment=Segment.S1,
                transition_mode=transition_mode.Immediate(),
            ),
        )

        for dev in autd.geometry():
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S1, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x81)

        autd.send(OutputMask.with_segment(lambda _dev: lambda _tr: False, Segment.S1))

        for dev in autd.geometry():
            intensities, phases = autd.link().drives_at(dev.idx(), Segment.S1, 0)
            assert np.all(intensities == 0x00)
            assert np.all(phases == 0x81)
