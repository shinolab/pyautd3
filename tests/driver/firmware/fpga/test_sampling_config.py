import pytest

from pyautd3 import SamplingConfig
from pyautd3.autd_error import AUTDError
from pyautd3.driver.common.freq import Hz
from pyautd3.utils import Duration


def test_sampl_config_from_freq_div():
    config = SamplingConfig(1)
    assert config.divide == 1
    assert config.freq() == 40000 * Hz
    assert config.period() == Duration.from_micros(25)

    with pytest.raises(AUTDError):
        _ = SamplingConfig(0)
    with pytest.raises(ValueError):  # noqa: PT011
        _ = SamplingConfig(0xFFFF + 1)


def test_sampl_config_from_freq():
    config = SamplingConfig(40000.0 * Hz)
    assert config.divide == 1
    assert config.freq() == 40000.0 * Hz
    assert config.period() == Duration.from_micros(25)

    with pytest.raises(AUTDError) as e:
        _ = SamplingConfig(39999.0 * Hz).divide
    assert str(e.value) == "Sampling frequency (39999 Hz) must divide the ultrasound frequency"

    with pytest.raises(AUTDError) as e:
        _ = SamplingConfig(39999.0 * Hz).freq()
    assert str(e.value) == "Sampling frequency (39999 Hz) must divide the ultrasound frequency"

    with pytest.raises(AUTDError) as e:
        _ = SamplingConfig(39999.0 * Hz).period()
    assert str(e.value) == "Sampling frequency (39999 Hz) must divide the ultrasound frequency"


def test_sampl_config_from_freq_nearest():
    config = SamplingConfig(40000.0 * Hz).into_nearest()
    assert config.divide == 1
    assert config.freq() == 40000 * Hz
    assert config.period() == Duration.from_micros(25)

    with pytest.raises(TypeError):
        _ = SamplingConfig(40000 * Hz).into_nearest()


def test_sampl_config_from_period():
    config = SamplingConfig(Duration.from_micros(25))
    assert config.divide == 1
    assert config.freq() == 40000 * Hz
    assert config.period() == Duration.from_micros(25)


def test_sampl_config_from_period_nearest():
    config = SamplingConfig(Duration.from_micros(25)).into_nearest()
    assert config.divide == 1
    assert config.freq() == 40000 * Hz
    assert config.period() == Duration.from_micros(25)


def test_sampl_config_ctor():
    with pytest.raises(TypeError):
        _ = SamplingConfig(0.0)  # type: ignore[arg-type]
