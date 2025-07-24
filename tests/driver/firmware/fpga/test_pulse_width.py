import pytest

from pyautd3.autd_error import AUTDError
from pyautd3.driver.firmware.fpga.pulse_width import PulseWidth


def test_pulse_width_from_duty():
    for i in range(512):
        _ = PulseWidth.from_duty(i / 512)

    with pytest.raises(AUTDError):
        _ = PulseWidth.from_duty(-1)

    with pytest.raises(AUTDError):
        _ = PulseWidth.from_duty(1)
