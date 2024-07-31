from collections.abc import Callable
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import ArrayLike

from pyautd3 import Controller, Device, Drive, Geometry, Segment, Transducer
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.gain import Gain
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3.link.audit import Audit


class Uniform(Gain):
    _intensity: EmitIntensity
    _phase: Phase
    check: np.ndarray

    def __init__(self: "Uniform", intensity: EmitIntensity, phase: Phase, check: ArrayLike) -> None:
        self._intensity = intensity
        self._phase = phase
        self.check = np.array(check)

    def calc(self: "Uniform", _: Geometry) -> Callable[[Device], Callable[[Transducer], Drive | EmitIntensity | Phase | tuple]]:
        def f(dev: Device) -> Callable[[Transducer], Drive | EmitIntensity | Phase | tuple]:
            self.check[dev.idx] = True
            return lambda _: Drive((self._phase, self._intensity))

        return Gain._transform(f)


def test_gain():
    autd: Controller[Audit]
    with create_controller() as autd:
        check = np.zeros(autd.geometry.num_devices, dtype=bool)
        autd.send(Uniform(EmitIntensity(0x80), Phase(0x90), check))

        for dev in autd.geometry:
            intensities, phases = autd.link.drives(dev.idx, Segment.S0, 0)
            assert np.all(intensities == 0x80)
            assert np.all(phases == 0x90)


def test_gain_check_only_for_enabled():
    autd: Controller[Audit]
    with create_controller() as autd:
        autd.geometry[0].enable = False

        check = np.zeros(autd.geometry.num_devices, dtype=bool)
        g = Uniform(EmitIntensity(0x80), Phase(0x90), check)
        autd.send(g)

        assert not g.check[0]
        assert g.check[1]

        intensities, phases = autd.link.drives(0, Segment.S0, 0)
        assert np.all(intensities == 0)
        assert np.all(phases == 0)

        intensities, phases = autd.link.drives(1, Segment.S0, 0)
        assert np.all(intensities == 0x80)
        assert np.all(phases == 0x90)
