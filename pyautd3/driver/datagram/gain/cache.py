from typing import Generic, Self, TypeVar

from pyautd3.driver.datagram.gain.base import GainBase
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_segment import IntoDatagramWithSegment
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import GainCachePtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr

G = TypeVar("G", bound=GainBase)


class Cache(
    IntoDatagramWithTimeout["Cache[G]"],
    IntoDatagramWithParallelThreshold["Cache[G]"],
    GainBase,
    IntoDatagramWithSegment["Cache[G]"],
    Generic[G],
):
    _g: G
    _ptr: GainCachePtr | None

    def __init__(self: Self, g: G) -> None:
        super().__init__()
        self._g = g
        self._ptr = None

    def _gain_ptr(self: Self, geometry: Geometry) -> GainPtr:
        if self._ptr is None:
            self._ptr = Base().gain_cache(self._g._gain_ptr(geometry))
        return Base().gain_cache_clone(self._ptr)

    def __del__(self: Self) -> None:
        if self._ptr is not None:
            Base().gain_cache_free(self._ptr)


class IntoGainCache(GainBase, Generic[G]):
    def with_cache(self: G) -> Cache[G]:
        return Cache(self)
