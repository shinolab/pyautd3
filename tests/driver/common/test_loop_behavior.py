import pytest

from pyautd3.autd_error import CantBeZeroError
from pyautd3.driver.common import LoopBehavior


def test_loop_behavior():
    with pytest.raises(NotImplementedError):
        _ = LoopBehavior()

    with pytest.raises(CantBeZeroError):
        _ = LoopBehavior.finite(0)

    assert LoopBehavior.finite(1) == LoopBehavior.once()
    assert LoopBehavior.finite(1) != LoopBehavior.infinite()
    assert LoopBehavior.finite(1) != 1
