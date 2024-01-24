import pytest

from pyautd3.gain.holo import Amplitude, dB, pascal


def test_holo_amp_db():
    amp = 121.5 * dB
    assert amp.pascal == 23.77004454874038
    assert amp.spl == 121.5


def test_holo_amp_pascal():
    amp = 23.77004454874038 * pascal
    assert amp.pascal == 23.77004454874038
    assert amp.spl == 121.5


def test_holo_amp_ctr():
    with pytest.raises(NotImplementedError):
        _ = Amplitude()

    with pytest.raises(NotImplementedError):
        _ = Amplitude._UnitPascal()

    with pytest.raises(NotImplementedError):
        _ = Amplitude._UnitSPL()
