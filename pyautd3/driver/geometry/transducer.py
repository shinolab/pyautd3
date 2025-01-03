from typing import Self

import numpy as np

from pyautd3.derive.derive_builder import builder
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import (
    DevicePtr,
    TransducerPtr,
)


@builder
class Transducer:
    _prop_idx: int
    _prop_dev_idx: int
    _ptr: TransducerPtr

    def __init__(self: Self, idx: int, dev_idx: int, ptr: DevicePtr) -> None:
        self._prop_idx = idx
        self._prop_dev_idx = dev_idx
        self._ptr = Base().transducer(ptr, idx)

    @property
    def position(self: Self) -> np.ndarray:
        return Base().transducer_position(self._ptr).ndarray()
