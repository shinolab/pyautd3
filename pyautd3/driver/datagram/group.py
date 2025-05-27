import ctypes
from collections.abc import Callable
from typing import Generic, Self, TypeVar

import numpy as np

from pyautd3.autd_error import InvalidDatagramTypeError
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.geometry import Device, Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, GeometryPtr

K = TypeVar("K")


class Group(Datagram, Generic[K]):
    def __init__(
        self: Self,
        key_map: Callable[[Device], K | None],
        data_map: dict[K, Datagram | tuple[Datagram, Datagram]],
    ) -> None:
        super().__init__()

        self._key_map = key_map
        self._data_map = data_map

    def _datagram_ptr(self: Self, geometry: Geometry) -> DatagramPtr:
        keymap: dict[K, int] = {}
        datagrams: np.ndarray = np.ndarray(len(self._data_map), dtype=DatagramPtr)
        keys = np.arange(len(self._data_map), dtype=np.int32)

        for k, (key, d) in enumerate(self._data_map.items()):
            match d:
                case Datagram():
                    ptr = d._datagram_ptr(geometry)
                    datagrams[k]["value"] = ptr.value
                case (Datagram(), Datagram()):
                    (d1, d2) = d
                    ptr = Base().datagram_tuple(
                        d1._datagram_ptr(geometry),
                        d2._datagram_ptr(geometry),
                    )
                    datagrams[k]["value"] = ptr.value
                case _:
                    raise InvalidDatagramTypeError
            keymap[key] = k

        def f_native(_context: ctypes.c_void_p, geometry_ptr: GeometryPtr, dev_idx: int) -> int:
            dev = Device(dev_idx, geometry_ptr)
            key = self._key_map(dev)
            return keymap[key] if key is not None else -1

        self.f_native_ = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p, GeometryPtr, ctypes.c_uint16)(f_native)

        return Base().datagram_group(
            self.f_native_,  # type: ignore[arg-type]
            ctypes.c_void_p(0),
            geometry._geometry_ptr,
            keys.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),  # type: ignore[arg-type]
            datagrams.ctypes.data_as(ctypes.POINTER(DatagramPtr)),  # type: ignore[arg-type]
            len(keys),
        )
