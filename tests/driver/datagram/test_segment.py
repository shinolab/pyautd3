import pytest

from pyautd3.driver.datagram.segment import SwapSegment


def test_swap_segment_ctor():
    with pytest.raises(NotImplementedError):
        _ = SwapSegment()

    with pytest.raises(NotImplementedError):
        _ = SwapSegment._Gain()

    with pytest.raises(NotImplementedError):
        _ = SwapSegment._Modulation()

    with pytest.raises(NotImplementedError):
        _ = SwapSegment._FociSTM()

    with pytest.raises(NotImplementedError):
        _ = SwapSegment._GainSTM()
