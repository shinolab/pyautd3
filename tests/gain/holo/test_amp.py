import pytest

from pyautd3.gain.holo import Amplitude, Pa, dB


def test_holo_amp_db():
    amp = 121.5 * dB
    assert amp.pascal == 23.77004454874038
    assert amp.spl == 121.5


def test_holo_amp_pascal():
    amp = 23.77004454874038 * Pa
    assert amp.pascal == 23.77004454874038
    assert amp.spl == 121.5


def test_holo_amp_ctr():
    with pytest.raises(NotImplementedError):
        _ = Amplitude()
