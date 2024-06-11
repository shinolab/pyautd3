import pytest

from pyautd3.driver.datagram.segment import SwapSegment


def test_swap_segment_ctor():
    with pytest.raises(NotImplementedError):
        _ = SwapSegment()
