from abc import ABCMeta, abstractmethod
from ctypes import POINTER, c_uint8
from typing import Generic, TypeVar

import numpy as np

from pyautd3.driver.common import SamplingConfiguration
from pyautd3.driver.datagram.modulation.modulation import Modulation as _Modulation
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import ModulationPtr

M = TypeVar("M", bound="Modulation")


class Modulation(_Modulation[M], Generic[M], metaclass=ABCMeta):
    """Base class of custom Modulation."""

    def __init__(self: "Modulation", config: SamplingConfiguration) -> None:
        """Constructor.

        Arguments:
        ---------
            config: sampling configuration
            loop_behavior: loop behavior

        """
        super().__init__(config)

    @abstractmethod
    def calc(self: "Modulation") -> np.ndarray:
        """Calculate modulation data."""

    def _modulation_ptr(self: "Modulation") -> ModulationPtr:
        data = np.fromiter((m.value for m in self.calc()), dtype=c_uint8)
        size = len(data)
        return Base().modulation_custom(
            self._config._internal,
            data.ctypes.data_as(POINTER(c_uint8)),  # type: ignore[arg-type]
            size,
            self._loop_behavior._internal,
        )
