from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, TypeVar

from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.driver.common.sampling_config import SamplingConfiguration
from pyautd3.driver.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr, ModulationPtr
from pyautd3.native_methods.utils import _validate_int

if TYPE_CHECKING:
    from pyautd3.modulation.cache import Cache
    from pyautd3.modulation.radiation_pressure import RadiationPressure
    from pyautd3.modulation.transform import Transform

__all__ = []  # type: ignore[var-annotated]

M = TypeVar("M", bound="IModulation")
MF = TypeVar("MF", bound="IModulationWithSamplingConfig")


class IModulation(Datagram, metaclass=ABCMeta):
    def __init__(self: "IModulation") -> None:
        super().__init__()

    def _datagram_ptr(self: "IModulation", _: Geometry) -> DatagramPtr:
        return Base().modulation_into_datagram(self._modulation_ptr())

    @property
    def sampling_config(self: "IModulation") -> SamplingConfiguration:
        return SamplingConfiguration.__private_new__(Base().modulation_sampling_config(self._modulation_ptr()))

    def __len__(self: "IModulation") -> int:
        return _validate_int(Base().modulation_size(self._modulation_ptr()))

    @abstractmethod
    def _modulation_ptr(self: "IModulation") -> ModulationPtr:
        pass

    def with_cache(self: M) -> "Cache":  # type: ignore[empty-body]
        # This function is implemented in cache.py
        pass

    def with_transform(self: M, f: Callable[[int, EmitIntensity], EmitIntensity]) -> "Transform":  # type: ignore[empty-body]
        # This function is implemented in transform.py
        pass

    def with_radiation_pressure(self: M) -> "RadiationPressure":  # type: ignore[empty-body]
        # This function is implemented in radiation_pressure.py
        pass


class IModulationWithSamplingConfig(IModulation):
    _config: SamplingConfiguration

    def __init__(self: "IModulationWithSamplingConfig", config: SamplingConfiguration) -> None:
        super().__init__()
        self._config = config

    def with_sampling_config(self: MF, config: SamplingConfiguration) -> MF:
        """Set sampling configuration.

        Arguments:
        ---------
            config: Sampling frequency configuration.
        """
        self._config = config
        return self
