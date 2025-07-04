from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np

from pyautd3 import Controller, Segment
from pyautd3.driver.firmware.fpga import Drive, Intensity, Phase
from pyautd3.driver.geometry import Device, Transducer
from pyautd3.gain import Custom
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


def test_custom():
    autd: Controller[Audit]
    with create_controller() as autd:

        def f(dev: Device) -> Callable[[Transducer], Drive]:
            if dev.idx() == 0:
                return lambda tr: Drive(phase=Phase(0x90), intensity=Intensity(0x80)) if tr.idx() == 0 else Drive.NULL
            if dev.idx() == 1:
                return lambda tr: Drive(phase=Phase(0x91), intensity=Intensity(0x81)) if tr.idx() == 248 else Drive.NULL
            return lambda _: Drive.NULL

        autd.send(Custom(f))

        intensities, phases = autd.link().drives_at(0, Segment.S0, 0)
        print(intensities)
        assert intensities[0] == 0x80
        assert phases[0] == 0x90
        assert np.all(intensities[1:-1] == 0)
        assert np.all(phases[1:-1] == 0)

        intensities, phases = autd.link().drives_at(1, Segment.S0, 0)
        assert intensities[-1] == 0x81
        assert phases[-1] == 0x91
        assert np.all(intensities[:-1] == 0)
        assert np.all(phases[:-1] == 0)
