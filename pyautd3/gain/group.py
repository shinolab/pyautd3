from collections.abc import Callable
from ctypes import POINTER, c_int32, c_uint16
from typing import Generic, Self, TypeVar

import numpy as np

from pyautd3.autd_error import UnknownGroupKeyError
from pyautd3.derive import datagram, gain
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr

K = TypeVar("K")


@gain
@datagram_with_segment
@datagram
class Group(Gain, Generic[K]):
    _map: dict[K, Gain]
    _f: Callable[[Device], Callable[[Transducer], K | None]]

    def __init__(self: Self, f: Callable[[Device], Callable[[Transducer], K | None]]) -> None:
        super().__init__()
        self._map = {}
        self._f = f
        self._parallel = False

    def set(self: Self, key: K, gain: Gain) -> "Group[K]":
        self._map[key] = gain
        return self

    def _gain_ptr(self: Self, geometry: Geometry) -> GainPtr:
        keymap: dict[K, int] = {}

        device_indices = np.array([dev.idx for dev in geometry])

        gain_group_map = Base().gain_group_create_map(np.ctypeslib.as_ctypes(device_indices.astype(c_uint16)), len(device_indices))
        k: int = 0
        for dev in geometry.devices:
            f = self._f(dev)
            m = np.zeros(dev.num_transducers, dtype=np.int32)
            for tr in dev:
                key = f(tr)
                if key is not None:
                    if key not in keymap:
                        keymap[key] = k
                        k += 1
                    m[tr.idx] = keymap[key]
                else:
                    m[tr.idx] = -1
            gain_group_map = Base().gain_group_map_set(gain_group_map, dev.idx, np.ctypeslib.as_ctypes(m.astype(c_int32)))

        keys: np.ndarray = np.ndarray(len(self._map), dtype=np.int32)
        values: np.ndarray = np.ndarray(len(self._map), dtype=GainPtr)
        for i, (key, value) in enumerate(self._map.items()):
            if key not in keymap:
                raise UnknownGroupKeyError
            keys[i] = keymap[key]
            values[i]["_0"] = value._gain_ptr(geometry)._0
        return Base().gain_group(
            gain_group_map,
            np.ctypeslib.as_ctypes(keys.astype(c_int32)),
            values.ctypes.data_as(POINTER(GainPtr)),  # type: ignore[arg-type]
            len(keys),
        )
