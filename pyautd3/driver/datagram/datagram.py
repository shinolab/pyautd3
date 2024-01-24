from abc import ABCMeta, abstractmethod

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_def import DatagramPtr

__all__ = []  # type: ignore[var-annotated]


class Datagram(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self: "Datagram") -> None:
        pass

    @abstractmethod
    def _datagram_ptr(self: "Datagram", geometry: Geometry) -> DatagramPtr:
        pass
