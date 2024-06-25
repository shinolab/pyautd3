import os

import pytest

from pyautd3 import AUTD3, Controller
from pyautd3.link.audit import Audit


@pytest.mark.dynamic_freq()
def test_builder_with_ultrasound_freq():
    f = os.getenv("AUTD3_ULTRASOUND_FREQ")
    freq = int(f) if f is not None else 40000

    autd: Controller[Audit] = Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(Audit.builder())

    for dev in autd.geometry:
        assert autd.link.ultrasound_freq(dev.idx) == freq
