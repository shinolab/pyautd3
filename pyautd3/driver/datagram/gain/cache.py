from ctypes import POINTER
from functools import reduce
from typing import Generic, TypeVar

import numpy as np

from pyautd3.driver.datagram.gain.base import GainBase
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_segment import IntoDatagramWithSegment
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import Drive, GainPtr
from pyautd3.native_methods.utils import _validate_ptr

G = TypeVar("G", bound=GainBase)


class Cache(
    IntoDatagramWithTimeout["Cache[G]"],
    IntoDatagramWithParallelThreshold["Cache[G]"],
    GainBase,
    IntoDatagramWithSegment["Cache[G]"],
    Generic[G],
):
    _g: G
    _cache: dict[int, np.ndarray]

    def __init__(self: "Cache[G]", g: G) -> None:
        super().__init__()
        self._g = g
        self._cache = {}

    def init(self: "Cache[G]", geometry: Geometry) -> None:
        device_indices = [dev.idx for dev in geometry.devices]

        if len(self._cache) != len(device_indices) or any(idx not in self._cache for idx in device_indices):
            gain_ptr = self._g._gain_ptr(geometry)
            res = _validate_ptr(Base().gain_calc(gain_ptr, geometry._geometry_ptr()))
            for dev in geometry.devices:
                drives = np.zeros(dev.num_transducers, dtype=Drive)
                Base().gain_calc_get_result(
                    res,
                    drives.ctypes.data_as(POINTER(Drive)),  # type: ignore[arg-type]
                    dev._ptr,
                )
                self._cache[dev.idx] = drives
            Base().gain_calc_free_result(res)
            Base().gain_free(gain_ptr)

    def _gain_ptr(self: "Cache[G]", geometry: Geometry) -> GainPtr:
        self.init(geometry)
        return reduce(
            lambda acc, dev: Base().gain_raw_set(
                acc,
                dev.idx,
                self._cache[dev.idx].ctypes.data_as(POINTER(Drive)),  # type: ignore[arg-type]
                len(self._cache[dev.idx]),
            ),
            geometry.devices,
            Base().gain_raw(),
        )

    @property
    def drives(self: "Cache[G]") -> dict[int, np.ndarray]:
        return self._cache


class IntoGainCache(GainBase, Generic[G]):
    def with_cache(self: G) -> "Cache[G]":
        return Cache(self)
