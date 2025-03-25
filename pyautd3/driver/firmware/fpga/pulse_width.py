from typing import Self


class PulseWidth:
    pulse_width: int

    def __init__(self: Self, pulse_width: int) -> None:
        if 0 <= pulse_width < 512:  # noqa: PLR2004
            self.pulse_width = pulse_width
        else:
            msg = "The pulse width must be in the range of 0 to 511."
            raise ValueError(msg)

    @staticmethod
    def from_duty(duty: float) -> "PulseWidth":
        return PulseWidth(int(512 * duty))
