from ctypes import c_double

import numpy as np

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import (
    DevicePtr,
    TransducerPtr,
)


class Transducer:
    _idx: int
    _ptr: TransducerPtr

    def __init__(self: "Transducer", idx: int, ptr: DevicePtr) -> None:
        self._idx = idx
        self._ptr = Base().transducer(ptr, idx)

    @property
    def idx(self: "Transducer") -> int:
        return self._idx

    @property
    def position(self: "Transducer") -> np.ndarray:
        v = np.zeros([3]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().transducer_position(self._ptr, vp)
        return v

    @property
    def rotation(self: "Transducer") -> np.ndarray:
        v = np.zeros([4]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().transducer_rotation(self._ptr, vp)
        return v

    @property
    def x_direction(self: "Transducer") -> np.ndarray:
        v = np.zeros([3]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().transducer_direction_x(self._ptr, vp)
        return v

    @property
    def y_direction(self: "Transducer") -> np.ndarray:
        v = np.zeros([3]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().transducer_direction_y(self._ptr, vp)
        return v

    @property
    def z_direction(self: "Transducer") -> np.ndarray:
        v = np.zeros([3]).astype(c_double)
        vp = np.ctypeslib.as_ctypes(v)
        Base().transducer_direction_z(self._ptr, vp)
        return v
