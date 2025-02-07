from collections.abc import Callable
from ctypes import POINTER, c_int32, c_uint16
from typing import Generic, Self, TypeVar

import numpy as np

from pyautd3.autd_error import UnknownGroupKeyError
from pyautd3.driver.datagram.gain import Gain
from pyautd3.driver.geometry import Device, Geometry, Transducer
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import GainPtr

K = TypeVar("K")


class Group(Gain, Generic[K]):
    key_map: Callable[[Device], Callable[[Transducer], K | None]]
    gain_map: dict[K, Gain]

    def __init__(self: Self, key_map: Callable[[Device], Callable[[Transducer], K | None]], gain_map: dict[K, Gain]) -> None:
        super().__init__()
        self.key_map = key_map
        self.gain_map = gain_map

    def _gain_ptr(self: Self, geometry: Geometry) -> GainPtr:
        keymap: dict[K, int] = {}

        device_indices = np.array([dev.idx() for dev in geometry])

        gain_group_map = Base().gain_group_create_map(np.ctypeslib.as_ctypes(device_indices.astype(c_uint16)), len(device_indices))
        k: int = 0
        for dev in geometry.devices():
            f = self.key_map(dev)
            m = np.zeros(dev.num_transducers(), dtype=np.int32)
            for tr in dev:
                key = f(tr)
                if key is not None:
                    if key not in keymap:
                        keymap[key] = k
                        k += 1
                    m[tr.idx()] = keymap[key]
                else:
                    m[tr.idx()] = -1
            gain_group_map = Base().gain_group_map_set(gain_group_map, dev.idx(), np.ctypeslib.as_ctypes(m.astype(c_int32)))

        keys: np.ndarray = np.ndarray(len(self.gain_map), dtype=np.int32)
        values: np.ndarray = np.ndarray(len(self.gain_map), dtype=GainPtr)
        for i, (key, value) in enumerate(self.gain_map.items()):
            if key not in keymap:
                raise UnknownGroupKeyError
            keys[i] = keymap[key]
            values[i]["value"] = value._gain_ptr(geometry).value
        return Base().gain_group(
            gain_group_map,
            np.ctypeslib.as_ctypes(keys.astype(c_int32)),
            values.ctypes.data_as(POINTER(GainPtr)),  # type: ignore[arg-type]
            len(keys),
        )
