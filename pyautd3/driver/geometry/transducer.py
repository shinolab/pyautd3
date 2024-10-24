from typing import Self

import numpy as np

from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import (
    DevicePtr,
    TransducerPtr,
)


class Transducer:
    _idx: int
    _dev_idx: int
    _ptr: TransducerPtr

    def __init__(self: Self, idx: int, dev_idx: int, ptr: DevicePtr) -> None:
        self._idx = idx
        self._dev_idx = dev_idx
        self._ptr = Base().transducer(ptr, idx)

    @property
    def idx(self: Self) -> int:
        return self._idx

    @property
    def dev_idx(self: Self) -> int:
        return self._dev_idx

    @property
    def position(self: Self) -> np.ndarray:
        return Base().transducer_position(self._ptr).ndarray()
