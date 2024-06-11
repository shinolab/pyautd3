import secrets
from typing import TYPE_CHECKING

import numpy as np

from pyautd3.driver.datagram.pulse_width_encoder import PulseWidthEncoder
from tests.test_autd import create_controller

if TYPE_CHECKING:
    from pyautd3 import Controller
    from pyautd3.link.audit import Audit


def test_pulse_width_encoder():
    autd: Controller[Audit]
    with create_controller() as autd:
        buf = np.array(sorted([secrets.randbelow(257) for _ in range(32768)]), dtype=np.uint16)
        autd.send(PulseWidthEncoder(lambda _: lambda i: buf[i]))
        for dev in autd.geometry:
            table = autd.link.pulse_width_encoder_table(dev.idx)
            assert np.array_equal(table, buf)

        buf_default = [np.round(np.arcsin(i / (255 * 255 // 2)) / np.pi * 512).astype(np.uint16) for i in range(255 * 255 // 2)]
        buf_default.extend([256] * (32768 - 255 * 255 // 2))
        autd.send(PulseWidthEncoder())
        for dev in autd.geometry:
            table = autd.link.pulse_width_encoder_table(dev.idx)
            assert np.array_equal(table, buf_default)
