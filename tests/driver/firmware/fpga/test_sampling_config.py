from datetime import timedelta

import pytest

from pyautd3 import SamplingConfig
from pyautd3.autd_error import AUTDError
from pyautd3.driver.defined.freq import Hz
from pyautd3.native_methods.autd3capi_driver import SamplingConfigTag


def test_sampl_config_from_freq_div():
    config = SamplingConfig.Division(512)
    assert config.division == 512
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)
    assert config._inner.tag == SamplingConfigTag.Division
    assert config._inner.value.div == 512


def test_sampl_config_from_freq_div_raw():
    config = SamplingConfig.DivisionRaw(512)
    assert config.division == 512
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)
    assert config._inner.tag == SamplingConfigTag.DivisionRaw
    assert config._inner.value.div == 512


def test_sampl_config_from_freq():
    config = SamplingConfig(40000 * Hz)
    assert config.division == 512
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)
    assert config._inner.tag == SamplingConfigTag.Freq
    assert config._inner.value.freq == 40000

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
    config = SamplingConfig.FreqNearest(40000.0 * Hz)
    assert config.division == 512
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)
    assert config._inner.tag == SamplingConfigTag.FreqNearest
    assert config._inner.value.freq_nearest == 40000.0


def test_sampl_config_from_period():
    config = SamplingConfig(timedelta(microseconds=25))
    assert config.division == 512
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)
    assert config._inner.tag == SamplingConfigTag.Period
    assert config._inner.value.period_ns == 25 * 1000


def test_sampl_config_from_period_nearest():
    config = SamplingConfig.PeriodNearest(timedelta(microseconds=25))
    assert config.division == 512
    assert config.freq == 40000 * Hz
    assert config.period == timedelta(microseconds=25)
    assert config._inner.tag == SamplingConfigTag.PeriodNearest
    assert config._inner.value.period_ns == 25 * 1000


def test_sampl_config_ctor():
    with pytest.raises(TypeError):
        _ = SamplingConfig(0.0)  # type: ignore[arg-type]
