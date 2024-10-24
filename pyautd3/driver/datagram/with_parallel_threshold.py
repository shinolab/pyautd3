from abc import ABCMeta
from typing import Generic, Self, TypeVar

from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr

from .datagram import Datagram

__all__ = []  # type: ignore[var-annotated]

D = TypeVar("D", bound="Datagram")


class DatagramWithParallelThreshold(Datagram, Generic[D]):
    _datagram: D
    _threshold: int | None

    def __init__(self: Self, datagram: D, threshold: int | None) -> None:
        self._datagram = datagram
        self._threshold = threshold

    def _datagram_ptr(self: Self, g: Geometry) -> DatagramPtr:
        raw_ptr = self._datagram._datagram_ptr(g)
        return Base().datagram_with_parallel_threshold(raw_ptr, self._threshold if self._threshold is not None else -1)


class IntoDatagramWithParallelThreshold(Generic[D], metaclass=ABCMeta):
    def with_parallel_threshold(self: D, threshold: int | None) -> DatagramWithParallelThreshold[D]:  # type: ignore[misc]
        return DatagramWithParallelThreshold(self, threshold)
