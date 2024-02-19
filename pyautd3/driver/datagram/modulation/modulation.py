from abc import ABCMeta, abstractmethod
from typing import TypeVar

from pyautd3.driver.common import LoopBehavior, SamplingConfiguration
from pyautd3.driver.datagram import Datagram
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr, ModulationPtr
from pyautd3.native_methods.utils import _validate_int

__all__ = []  # type: ignore[var-annotated]

M = TypeVar("M", bound="IModulation")
MF = TypeVar("MF", bound="IModulationWithSamplingConfig")
ML = TypeVar("ML", bound="IModulationWithLoopBehavior")


class IModulation(Datagram, metaclass=ABCMeta):
    _loop_behavior: LoopBehavior

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


class IModulationWithLoopBehavior(IModulation):
    def __init__(self: "IModulationWithLoopBehavior") -> None:
        super().__init__()
        self._loop_behavior = LoopBehavior.infinite()

    def with_loop_behavior(self: ML, loop_behavior: LoopBehavior) -> ML:
        """Set loop behavior.

        Arguments:
        ---------
            loop_behavior: Loop behavior.

        """
        self._loop_behavior = loop_behavior
        return self
