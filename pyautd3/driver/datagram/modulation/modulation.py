from abc import ABCMeta
from datetime import timedelta
from typing import Generic, Self, TypeVar

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.fir import IntoModulationFir
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig

__all__ = []  # type: ignore[var-annotated]

M = TypeVar("M", bound="Modulation")


class Modulation(
    IntoModulationCache[M],
    IntoModulationRadiationPressure[M],
    IntoModulationFir[M],
    ModulationBase[M],
    Generic[M],
    metaclass=ABCMeta,
):
    _config: SamplingConfig

    def __init__(self: Self, config: SamplingConfig | Freq[int] | Freq[float] | timedelta) -> None:
        super().__init__()
        self._config = SamplingConfig(config)

    def with_sampling_config(self: M, config: SamplingConfig | Freq[int] | Freq[float] | timedelta) -> M:
        self._config = SamplingConfig(config)
        return self
