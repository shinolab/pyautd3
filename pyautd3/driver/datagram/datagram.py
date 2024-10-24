from abc import ABCMeta, abstractmethod
from typing import Self

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import DatagramPtr

__all__ = []  # type: ignore[var-annotated]


class Datagram(metaclass=ABCMeta):
    @abstractmethod
    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        pass
