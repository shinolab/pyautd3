from abc import ABCMeta
from typing import Generic, TypeVar

from pyautd3.driver.datagram.gain.base import GainBase
from pyautd3.driver.datagram.gain.cache import IntoGainCache
from pyautd3.driver.datagram.gain.transform import IntoGainTransform
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_segment import IntoDatagramWithSegment
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout

__all__ = []  # type: ignore[var-annotated]

G = TypeVar("G", bound="Gain")


class Gain(
    IntoDatagramWithTimeout[G],
    IntoDatagramWithParallelThreshold[G],
    IntoDatagramWithSegment[G],
    IntoGainCache[G],
    IntoGainTransform[G],
    GainBase,
    Generic[G],
    metaclass=ABCMeta,
):
    def __init__(self: "Gain[G]") -> None:
        super().__init__()
