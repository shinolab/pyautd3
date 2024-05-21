import pytest

from pyautd3.driver.defined import Freq, Hz, kHz
from pyautd3.driver.defined.freq import _UnitHz, _UnitkHz


def test_freq_int():
    freq = 1 * Hz
    assert freq.hz == 1

    freq = 1 * kHz
    assert freq.hz == 1000


def test_freq_float():
    freq = 1.0 * Hz
    assert freq.hz == 1.0

    freq = 1.0 * kHz
    assert freq.hz == 1000.0


def test_freq_ctor():
    with pytest.raises(NotImplementedError):
        _ = Freq()

    with pytest.raises(NotImplementedError):
        _ = _UnitHz()

    with pytest.raises(NotImplementedError):
        _ = _UnitkHz()
