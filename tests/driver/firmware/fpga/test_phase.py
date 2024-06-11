import numpy as np
import pytest

from pyautd3.driver.defined import rad
from pyautd3.driver.firmware.fpga import Phase


def test_phase():
    for i in range(256):
        phase = Phase(Phase(i))
        assert phase.value == i
        assert str(phase) == f"Phase({i})"

    phase = Phase(0.0 * rad)
    assert phase.radian == 0
    phase = Phase(np.pi * rad)
    assert phase.radian == 3.1415927410125732
    phase = Phase(2 * np.pi * rad)
    assert phase.radian == 0

    with pytest.raises(TypeError):
        _ = Phase(0.0)  # type: ignore[arg-type]
