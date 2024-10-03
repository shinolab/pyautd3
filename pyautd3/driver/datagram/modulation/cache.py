from ctypes import POINTER, c_uint8
from typing import Generic, TypeVar

import numpy as np

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.native_methods.autd3capi import ModulationCalcPtr, ResultModulationCalc
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr
from pyautd3.native_methods.structs import SamplingConfig
from pyautd3.native_methods.utils import _validate_ptr

M = TypeVar("M", bound=ModulationBase)


class Cache(ModulationBase["Cache[M]"], Generic[M]):
    _m: M
    _cache: np.ndarray | None
    _sampling_config: SamplingConfig | None

    def __init__(self: "Cache[M]", m: M) -> None:
        super().__init__()
        self._m = m
        self._cache = None
        self._sampling_config = None
        self._loop_behavior = m._loop_behavior

    def _init(self: "Cache[M]") -> np.ndarray:
        if self._cache is None:
            res: ResultModulationCalc = Base().modulation_calc(self._m._modulation_ptr())
            ptr: ModulationCalcPtr = _validate_ptr(res)
            buf = np.zeros(int(Base().modulation_calc_get_size(ptr)), dtype=c_uint8)
            self._sampling_config = res.config
            Base().modulation_calc_get_result(ptr, buf.ctypes.data_as(POINTER(c_uint8)))  # type: ignore[arg-type]
            Base().modulation_calc_free_result(ptr)
            self._cache = buf
        return self._cache

    def calc(self: "Cache[M]") -> np.ndarray:
        return self._init()

    def _modulation_ptr(self: "Cache[M]") -> ModulationPtr:
        data = np.fromiter((m for m in self.calc()), dtype=c_uint8)
        size = len(data)
        return Base().modulation_custom(
            self._sampling_config,  # type: ignore[arg-type]
            self._loop_behavior,
            data.ctypes.data_as(POINTER(c_uint8)),  # type: ignore[arg-type]
            size,
        )

    @property
    def buffer(self: "Cache[M]") -> np.ndarray | None:
        return self._cache


class IntoModulationCache(ModulationBase[M], Generic[M]):
    def with_cache(self: M) -> "Cache[M]":
        return Cache(self)
