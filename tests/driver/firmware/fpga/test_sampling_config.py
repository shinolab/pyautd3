from datetime import timedelta

import pytest

from pyautd3 import SamplingConfig
from pyautd3.autd_error import AUTDError
from pyautd3.driver.defined.freq import Freq, Hz


def test_sampl_config_from_freq_div():
    config = SamplingConfig(1)
    assert config.division == 1
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)

    with pytest.raises(ValueError):  # noqa: PT011
        _ = SamplingConfig(0)
    with pytest.raises(ValueError):  # noqa: PT011
        _ = SamplingConfig(0xFFFF + 1)


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

    with pytest.raises(TypeError):
        _ = SamplingConfig(Freq.__private_new__(1j))


def test_sampl_config_from_freq_f():
    config = SamplingConfig(40000.0 * Hz)
    assert config.division == 1
    assert config.freq == 40000.0 * Hz
    assert config.period == timedelta(microseconds=25)

    with pytest.raises(AUTDError) as e:
        _ = SamplingConfig(39999.0 * Hz).division
    assert str(e.value) == "Sampling frequency (39999 Hz) must divide 40000 Hz"

    with pytest.raises(AUTDError) as e:
        _ = SamplingConfig(39999.0 * Hz).freq
    assert str(e.value) == "Sampling frequency (39999 Hz) must divide 40000 Hz"

    with pytest.raises(AUTDError) as e:
        _ = SamplingConfig(39999.0 * Hz).period
    assert str(e.value) == "Sampling frequency (39999 Hz) must divide 40000 Hz"


def test_sampl_config_from_freq_nearest():
    config = SamplingConfig.nearest(40000.0 * Hz)
    assert config.division == 1
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)

    with pytest.raises(TypeError):
        _ = SamplingConfig.nearest(40000 * Hz)

    with pytest.raises(TypeError):
        _ = SamplingConfig.nearest(40000)  # type: ignore[arg-type]


def test_sampl_config_from_period():
    config = SamplingConfig(timedelta(microseconds=25))
    assert config.division == 1
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)


def test_sampl_config_from_period_nearest():
    config = SamplingConfig.nearest(timedelta(microseconds=25))
    assert config.division == 1
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)


def test_sampl_config_ctor():
    with pytest.raises(TypeError):
        _ = SamplingConfig(0.0)  # type: ignore[arg-type]
