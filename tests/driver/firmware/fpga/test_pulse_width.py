import pytest

from pyautd3.autd_error import AUTDError
from pyautd3.driver.firmware.fpga.pulse_width import PulseWidth


def test_pulse_width():
    for i in range(512):
        assert PulseWidth(i).pulse_width == i

    with pytest.raises(AUTDError):
        _ = PulseWidth(-1)

    with pytest.raises(AUTDError):
        _ = PulseWidth(512)


def test_pulse_width_from_duty():
    for i in range(512):
        assert PulseWidth.from_duty(i / 512).pulse_width == i

    with pytest.raises(AUTDError):
        _ = PulseWidth.from_duty(-1)

    with pytest.raises(AUTDError):
        _ = PulseWidth.from_duty(1)
