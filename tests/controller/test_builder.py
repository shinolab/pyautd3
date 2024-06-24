from pyautd3 import AUTD3, Controller, kHz, set_ultrasound_freq
from pyautd3.link.audit import Audit


def test_builder_with_ultrasound_freq():
    set_ultrasound_freq(41 * kHz)

    autd: Controller[Audit] = Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(Audit.builder())

    for dev in autd.geometry:
        assert autd.link.ultrasound_freq(dev.idx) == 41000

    set_ultrasound_freq(40 * kHz)
