from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, TypeVar

from pyautd3.driver.common.drive import Drive
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr, GainPtr, Segment

from .with_segment import DatagramS

if TYPE_CHECKING:
    from pyautd3.gain.cache import Cache
    from pyautd3.gain.transform import Transform

__all__ = []  # type: ignore[var-annotated]

G = TypeVar("G", bound="IGain")


class IGain(DatagramS["IGain", GainPtr], metaclass=ABCMeta):
    def __init__(self: "IGain") -> None:
        super().__init__()

    def _raw_ptr(self: "IGain", geometry: Geometry) -> GainPtr:
        self._gain_ptr(geometry)

    def _into_segment(self: "IGain", ptr: GainPtr, segment: Segment, *, update_segment: bool) -> DatagramPtr:
        return Base().gain_into_datagram_with_segment(ptr, segment, update_segment)

    def _datagram_ptr(self: "IGain", geometry: Geometry) -> DatagramPtr:
        return Base().gain_into_datagram(self._gain_ptr(geometry))

    @abstractmethod
    def _gain_ptr(self: "IGain", geometry: Geometry) -> GainPtr:
        pass

    def with_cache(self: G) -> "Cache":  # type: ignore[empty-body]
        # This function is implemented in cache.py
        pass

    def with_transform(self: G, f: Callable[[Device, Transducer, Drive], Drive]) -> "Transform":  # type: ignore[empty-body]
        # This function is implemented in transform.py
        pass
