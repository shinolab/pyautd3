import pytest

from pyautd3 import SamplingConfig
from pyautd3.driver.defined.freq import Hz
from pyautd3.native_methods.autd3capi_driver import SamplingConfigTag


def test_sampl_config_from_freq_div():
    config = SamplingConfig.Division(512)
    assert config.tag == SamplingConfigTag.Division
    assert config.value.div == 512


def test_sampl_config_from_freq_div_raw():
    config = SamplingConfig.DivisionRaw(512)
    assert config.tag == SamplingConfigTag.DivisionRaw
    assert config.value.div == 512


def test_sampl_config_from_freq():
    config = SamplingConfig.Freq(4000 * Hz)
    assert config.tag == SamplingConfigTag.Freq
    assert config.value.freq == 4000


def test_sampl_config_from_freq_nearest():
    config = SamplingConfig.FreqNearest(4000.0 * Hz)
    assert config.tag == SamplingConfigTag.FreqNearest
    assert config.value.freq_nearest == 4000.0


def test_sampl_config_ctor():
    with pytest.raises(NotImplementedError):
        _ = SamplingConfig()
