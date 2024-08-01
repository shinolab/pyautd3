from abc import ABCMeta
from datetime import timedelta
from typing import Generic, TypeVar

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.datagram.modulation.transform import IntoModulationTransform
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig

__all__ = []  # type: ignore[var-annotated]

M = TypeVar("M", bound="Modulation")


class Modulation(
    IntoModulationCache[M],
    IntoModulationTransform[M],
    IntoModulationRadiationPressure[M],
    ModulationBase[M],
    Generic[M],
    metaclass=ABCMeta,
):
    _config: SamplingConfig

    def __init__(self: "Modulation[M]", config: SamplingConfig | Freq[int] | Freq[float] | timedelta) -> None:
        super().__init__()
        self._config = SamplingConfig(config)

    def with_sampling_config(self: M, config: SamplingConfig | Freq[int] | Freq[float] | timedelta) -> M:
        self._config = SamplingConfig(config)
        return self
