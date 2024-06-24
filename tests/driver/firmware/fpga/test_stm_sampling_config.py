from datetime import timedelta

import pytest

from pyautd3.autd_error import AUTDError
from pyautd3.driver.defined.freq import Hz
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.firmware.fpga.stm_sampling_config import STMSamplingConfig
from pyautd3.native_methods.autd3capi_driver import STMSamplingConfigTag


def test_stm_sampl_config_from_freq():
    config = STMSamplingConfig.Freq(40000.0 * Hz)
    assert config.freq(1) == 40000.0 * Hz
    assert config.period(1) == timedelta(microseconds=25)
    assert config.sampling_config(1) == SamplingConfig.Freq(40000 * Hz)
    assert config._inner.tag == STMSamplingConfigTag.Freq
    assert config._inner.value.freq == 40000

    with pytest.raises(AUTDError) as e:
        _ = STMSamplingConfig.Freq(0.1 * Hz).sampling_config(1)
    assert str(e.value) == "STM sampling frequency (0.1 Hz*1) must be integer"

    with pytest.raises(AUTDError) as e:
        _ = STMSamplingConfig.Freq(0.1 * Hz).freq(1)
    assert str(e.value) == "STM sampling frequency (0.1 Hz*1) must be integer"

    with pytest.raises(AUTDError) as e:
        _ = STMSamplingConfig.Freq(0.1 * Hz).period(1)
    assert str(e.value) == "STM sampling frequency (0.1 Hz*1) must be integer"


def test_stm_sampl_config_from_freq_nearest():
    config = STMSamplingConfig.FreqNearest(40000.0 * Hz)
    assert config.freq(1) == 40000.0 * Hz
    assert config.period(1) == timedelta(microseconds=25)
    assert config.sampling_config(1) == SamplingConfig.Freq(40000 * Hz)
    assert config._inner.tag == STMSamplingConfigTag.FreqNearest
    assert config._inner.value.freq == 40000.0


def test_stm_sampl_config_from_period():
    config = STMSamplingConfig.Period(timedelta(microseconds=25))
    assert config.freq(1) == 40000.0 * Hz
    assert config.period(1) == timedelta(microseconds=25)
    assert config.sampling_config(1) == SamplingConfig.Freq(40000 * Hz)
    assert config._inner.tag == STMSamplingConfigTag.Period
    assert config._inner.value.period_ns == 25 * 1000


def test_stm_sampl_config_from_period_nearest():
    config = STMSamplingConfig.PeriodNearest(timedelta(microseconds=25))
    assert config.freq(1) == 40000.0 * Hz
    assert config.period(1) == timedelta(microseconds=25)
    assert config.sampling_config(1) == SamplingConfig.Freq(40000 * Hz)
    assert config._inner.tag == STMSamplingConfigTag.PeriodNearest
    assert config._inner.value.period_ns == 25 * 1000


def test_stm_sampl_config_from_sampl_config():
    config = STMSamplingConfig.SamplingConfig(SamplingConfig.Freq(40000 * Hz))
    assert config.freq(1) == 40000.0 * Hz
    assert config.period(1) == timedelta(microseconds=25)
    assert config.sampling_config(1) == SamplingConfig.Freq(40000 * Hz)
    assert config._inner.tag == STMSamplingConfigTag.SamplingConfig
    assert config._inner.value.sampling_config == SamplingConfig.Freq(40000 * Hz)._inner
