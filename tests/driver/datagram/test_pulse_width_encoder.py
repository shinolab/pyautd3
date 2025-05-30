import secrets
from typing import TYPE_CHECKING

import numpy as np

from pyautd3.driver.datagram.pulse_width_encoder import PulseWidthEncoder
from pyautd3.driver.firmware.fpga.pulse_width import PulseWidth
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3 import Controller
    from pyautd3.link.audit import Audit


def test_pulse_width_encoder():
    autd: Controller[Audit]
    with create_controller() as autd:
        buf = np.array([secrets.randbelow(256) for _ in range(256)], dtype=np.uint16)
        autd.send(PulseWidthEncoder(lambda _: lambda i: PulseWidth(buf[i.value])))
        for dev in autd.geometry():
            table = autd.link().pulse_width_encoder_table(dev.idx())
            assert np.array_equal(table, buf)

        buf_default = [np.round(np.arcsin(i / 255) / np.pi * 512).astype(np.uint16) for i in range(256)]
        autd.send(PulseWidthEncoder())
        for dev in autd.geometry():
            table = autd.link().pulse_width_encoder_table(dev.idx())
            assert np.array_equal(table, buf_default)
