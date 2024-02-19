from typing import TYPE_CHECKING

import numpy as np
import pytest
from numpy.typing import ArrayLike

from pyautd3 import Controller, Device, Drive, Geometry, Segment, Transducer
from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.driver.common.phase import Phase
from pyautd3.gain import Gain
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


class Uniform(Gain):
    _intensity: EmitIntensity
    _phase: Phase
    check: np.ndarray

    def __init__(self: "Uniform", intensity: int, phase: Phase, check: ArrayLike) -> None:
        self._intensity = EmitIntensity(intensity)
        self._phase = phase
        self.check = np.array(check)

    def calc(self: "Uniform", geometry: Geometry) -> dict[int, np.ndarray]:
        def f(dev: Device, _tr: Transducer) -> Drive:
            self.check[dev.idx] = True
            return Drive(
                self._phase,
                self._intensity,
            )

        return Gain._transform(geometry, f)


@pytest.mark.asyncio()
async def test_gain():
    autd: Controller[Audit]
    with await create_controller() as autd:
        check = np.zeros(autd.geometry.num_devices, dtype=bool)
        assert await autd.send_async(Uniform(0x80, Phase(0x90), check))

        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x90)


@pytest.mark.asyncio()
async def test_gain_check_only_for_enabled():
    autd: Controller[Audit]
    with await create_controller() as autd:
        autd.geometry[0].enable = False

        check = np.zeros(autd.geometry.num_devices, dtype=bool)
        g = Uniform(0x80, Phase(0x90), check)
        assert await autd.send_async(g)

        assert not g.check[0]
        assert g.check[1]

        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 0x90)
