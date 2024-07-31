from datetime import timedelta

import pytest

from pyautd3 import SamplingConfig
from pyautd3.autd_error import AUTDError
from pyautd3.driver.defined.freq import Hz


def test_sampl_config_from_freq_div():
    config = SamplingConfig(1)
    assert config.division == 1
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)


def test_sampl_config_from_freq():
    config = SamplingConfig(40000 * Hz)
    assert config.division == 1
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)

    with pytest.raises(AUTDError) as e:
        _ = SamplingConfig(39999 * Hz).division
    assert str(e.value) == "Sampling frequency (39999 Hz) must divide 40000 Hz"

    with pytest.raises(AUTDError) as e:
        _ = SamplingConfig(39999 * Hz).freq
    assert str(e.value) == "Sampling frequency (39999 Hz) must divide 40000 Hz"

    with pytest.raises(AUTDError) as e:
        _ = SamplingConfig(39999 * Hz).period
    assert str(e.value) == "Sampling frequency (39999 Hz) must divide 40000 Hz"


def test_sampl_config_from_freq_nearest():
    config = SamplingConfig._nearest(40000.0 * Hz)
    assert config.division == 1
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)


def test_sampl_config_from_period():
    config = SamplingConfig(timedelta(microseconds=25))
    assert config.division == 1
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)


def test_sampl_config_from_period_nearest():
    config = SamplingConfig._nearest(timedelta(microseconds=25))
    assert config.division == 1
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)


def test_sampl_config_ctor():
    with pytest.raises(TypeError):
        _ = SamplingConfig(0.0)  # type: ignore[arg-type]
