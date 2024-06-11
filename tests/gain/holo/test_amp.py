import pytest

from pyautd3.gain.holo import Amplitude, Pa, dB


def test_holo_amp_db():
    amp = 121.5 * dB
    assert amp.pascal == 23.770034790039062
    assert amp.spl == 121.5


def test_holo_amp_pascal():
    amp = 23.770034790039062 * Pa
    assert amp.pascal == 23.770034790039062
    assert amp.spl == 121.5


def test_holo_amp_ctr():
    with pytest.raises(NotImplementedError):
        _ = Amplitude()

    with pytest.raises(NotImplementedError):
        _ = Amplitude._UnitPascal()

    with pytest.raises(NotImplementedError):
        _ = Amplitude._UnitSPL()
