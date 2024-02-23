from abc import ABCMeta
from typing import Generic, TypeVar

from pyautd3.driver.common import SamplingConfiguration
from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.datagram.modulation.transform import IntoModulationTransform

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
    _config: SamplingConfiguration

    def __init__(self: "Modulation[M]", config: SamplingConfiguration) -> None:
        super().__init__()
        self._config = config

    def with_sampling_config(self: M, config: SamplingConfiguration) -> M:
        """Set sampling configuration.

        Arguments:
        ---------
            config: Sampling frequency configuration.

        """
        self._config = config
        return self
