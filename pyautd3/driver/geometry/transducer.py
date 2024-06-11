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
        return Base().transducer_position(self._ptr).ndarray()
