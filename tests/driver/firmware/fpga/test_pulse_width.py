from pyautd3.driver.firmware.fpga.pulse_width import PulseWidth


def test_pulse_width_from_duty():
    for i in range(512):
        _ = PulseWidth.from_duty(i / 512)
