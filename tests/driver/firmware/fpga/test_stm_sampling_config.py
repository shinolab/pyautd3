from datetime import timedelta

import pytest

from pyautd3.autd_error import AUTDError
from pyautd3.driver.datagram.stm.stm_sampling_config import STMSamplingConfig
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig


def test_stm_sampl_config_from_freq():
    config = STMSamplingConfig(40000.0 * Hz, 1)
    assert config.freq() == 40000.0 * Hz
    assert config.period() == timedelta(microseconds=25)
    assert config.sampling_config() == SamplingConfig(40000 * Hz)

    with pytest.raises(AUTDError) as e:
        _ = STMSamplingConfig(0.1 * Hz, 1).sampling_config()
    assert str(e.value) == "Sampling frequency (0.1 Hz) is out of range ([0.61036086 Hz, 40000 Hz])"

    with pytest.raises(AUTDError) as e:
        _ = STMSamplingConfig(0.1 * Hz, 1).freq()
    assert str(e.value) == "Sampling frequency (0.1 Hz) is out of range ([0.61036086 Hz, 40000 Hz])"

    with pytest.raises(AUTDError) as e:
        _ = STMSamplingConfig(0.1 * Hz, 1).period()
    assert str(e.value) == "Sampling frequency (0.1 Hz) is out of range ([0.61036086 Hz, 40000 Hz])"

    with pytest.raises(TypeError):
        _ = STMSamplingConfig(1 * Hz, 1)

    with pytest.raises(TypeError):
        _ = STMSamplingConfig(1, 1)  # type: ignore[arg-type]


def test_stm_sampl_config_from_period():
    config = STMSamplingConfig(timedelta(microseconds=25), 1)
    assert config.freq() == 40000.0 * Hz
    assert config.period() == timedelta(microseconds=25)
    assert config.sampling_config() == SamplingConfig(40000 * Hz)


def test_stm_sampl_config_from_sampl_config():
    config = STMSamplingConfig(SamplingConfig(40000 * Hz), 1)
    assert config.freq() == 40000.0 * Hz
    assert config.period() == timedelta(microseconds=25)
    assert config.sampling_config() == SamplingConfig(40000 * Hz)


def test_stm_sampl_config_from_freq_nearest():
    config = STMSamplingConfig._nearest(40000.0 * Hz, 1)
    assert config.freq() == 40000.0 * Hz
    assert config.period() == timedelta(microseconds=25)
    assert config.sampling_config() == SamplingConfig(40000 * Hz)

    with pytest.raises(TypeError):
        _ = STMSamplingConfig._nearest(1 * Hz, 1)

    with pytest.raises(TypeError):
        _ = STMSamplingConfig._nearest(1, 1)  # type: ignore[arg-type]


def test_stm_sampl_config_from_period_nearest():
    config = STMSamplingConfig._nearest(timedelta(microseconds=25), 1)
    assert config.freq() == 40000.0 * Hz
    assert config.period() == timedelta(microseconds=25)
    assert config.sampling_config() == SamplingConfig(40000 * Hz)
