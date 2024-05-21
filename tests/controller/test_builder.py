from pyautd3 import AUTD3, Controller, kHz
from pyautd3.link.audit import Audit


def test_builder_with_ultrasound_freq():
    autd: Controller[Audit] = Controller.builder().add_device(AUTD3([0.0, 0.0, 0.0])).with_ultrasound_freq(41 * kHz).open(Audit.builder())

    for dev in autd.geometry:
        assert autd.link.ultrasound_freq(dev.idx) == 41000
