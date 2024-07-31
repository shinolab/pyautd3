import pytest

from pyautd3.autd_error import CantBeZeroError
from pyautd3.driver.firmware.fpga import LoopBehavior


def test_loop_behavior():
    with pytest.raises(NotImplementedError):
        _ = LoopBehavior()

    with pytest.raises(CantBeZeroError):
        _ = LoopBehavior.Finite(0)

    assert LoopBehavior.Finite(1) == LoopBehavior.Once
    assert LoopBehavior.Infinite.rep == 0xFFFF
    assert LoopBehavior.Finite(1).rep == 0
