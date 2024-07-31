from datetime import timedelta

import pytest

from pyautd3.autd_error import AUTDError
from pyautd3.driver.datagram.stm.stm_sampling_config import STMSamplingConfig
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.native_methods.autd3capi_driver import STMConfigTag


def test_stm_sampl_config_from_freq():
    config = STMSamplingConfig(40000.0 * Hz)
    assert config.freq(1) == 40000.0 * Hz
    assert config.period(1) == timedelta(microseconds=25)
    assert config.sampling_config(1) == SamplingConfig(40000 * Hz)
    assert config._inner.tag == STMConfigTag.Freq
    assert config._inner.value.freq == 40000.0

    with pytest.raises(AUTDError) as e:
        _ = STMSamplingConfig(0.1 * Hz).sampling_config(1)
    assert str(e.value) == "Sampling frequency (0.1 Hz) is out of range ([0.61036086 Hz, 40000 Hz])"

    with pytest.raises(AUTDError) as e:
        _ = STMSamplingConfig(0.1 * Hz).freq(1)
    assert str(e.value) == "Sampling frequency (0.1 Hz) is out of range ([0.61036086 Hz, 40000 Hz])"

    with pytest.raises(AUTDError) as e:
        _ = STMSamplingConfig(0.1 * Hz).period(1)
    assert str(e.value) == "Sampling frequency (0.1 Hz) is out of range ([0.61036086 Hz, 40000 Hz])"


def test_stm_sampl_config_from_period():
    config = STMSamplingConfig(timedelta(microseconds=25))
    assert config.freq(1) == 40000.0 * Hz
    assert config.period(1) == timedelta(microseconds=25)
    assert config.sampling_config(1) == SamplingConfig(40000 * Hz)
    assert config._inner.tag == STMConfigTag.Period
    assert config._inner.value.period_ns == 25 * 1000


def test_stm_sampl_config_from_sampl_config():
    config = STMSamplingConfig(SamplingConfig(40000 * Hz))
    assert config.freq(1) == 40000.0 * Hz
    assert config.period(1) == timedelta(microseconds=25)
    assert config.sampling_config(1) == SamplingConfig(40000 * Hz)
    assert config._inner.tag == STMConfigTag.SamplingConfig
    assert config._inner.value.sampling_config.div == SamplingConfig(40000 * Hz)._inner.div


def test_stm_sampl_config_from_freq_nearest():
    config = STMSamplingConfig._nearest(40000.0 * Hz)
    assert config.freq(1) == 40000.0 * Hz
    assert config.period(1) == timedelta(microseconds=25)
    assert config.sampling_config(1) == SamplingConfig(40000 * Hz)
    assert config._inner.tag == STMConfigTag.FreqNearest
    assert config._inner.value.freq == 40000.0


def test_stm_sampl_config_from_period_nearest():
    config = STMSamplingConfig._nearest(timedelta(microseconds=25))
    assert config.freq(1) == 40000.0 * Hz
    assert config.period(1) == timedelta(microseconds=25)
    assert config.sampling_config(1) == SamplingConfig(40000 * Hz)
    assert config._inner.tag == STMConfigTag.PeriodNearest
    assert config._inner.value.period_ns == 25 * 1000
