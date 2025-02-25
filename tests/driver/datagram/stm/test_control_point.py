import numpy as np

from pyautd3.driver.datagram.stm.control_point import ControlPoint
from pyautd3.driver.firmware.fpga.phase import Phase


def test_control_point():
    c = ControlPoint(point=[1.0, 2.0, 3.0], phase_offset=Phase(0x80))
    assert np.array_equal(c.point, [1.0, 2.0, 3.0])
    assert c.phase_offset == Phase(0x80)
