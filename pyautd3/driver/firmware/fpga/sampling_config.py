from pyautd3.driver.defined import Freq as _Freq
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import SamplingConfigWrap


class SamplingConfig:
    @staticmethod
    def Freq(freq: _Freq[int]) -> SamplingConfigWrap:  # noqa: N802
        return Base().sampling_config_from_freq(freq.hz)

    @staticmethod
    def FreqNearest(freq: _Freq[float]) -> SamplingConfigWrap:  # noqa: N802
        return Base().sampling_config_from_freq_nearest(freq.hz)

    @staticmethod
    def Division(div: int) -> SamplingConfigWrap:  # noqa: N802
        return Base().sampling_config_from_division(div)

    @staticmethod
    def DivisionRaw(div: int) -> SamplingConfigWrap:  # noqa: N802
        return Base().sampling_config_from_division_raw(div)

    def __new__(cls: type["SamplingConfig"]) -> "SamplingConfig":
        raise NotImplementedError
