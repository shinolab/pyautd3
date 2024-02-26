from ctypes import POINTER, c_uint8
from typing import Generic, TypeVar

import numpy as np

from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.driver.common.sampling_config import SamplingConfiguration
from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import ModulationPtr
from pyautd3.native_methods.utils import _validate_ptr

M = TypeVar("M", bound=ModulationBase)


class Cache(ModulationBase["Cache[M]"], Generic[M]):
    """Modulation to cache the result of calculation."""

    _m: M
    _cache: np.ndarray | None
    _sampling_config: SamplingConfiguration | None

    def __init__(self: "Cache[M]", m: M) -> None:
        super().__init__()
        self._m = m
        self._cache = None
        self._sampling_config = None
        self._loop_behavior = m._loop_behavior

    def _init(self: "Cache[M]") -> np.ndarray:
        if self._cache is None:
            ptr = Base().modulation_calc(self._m._modulation_ptr())
            res = _validate_ptr(ptr)
            buf = np.zeros(int(ptr.result_len), dtype=c_uint8)
            self._sampling_config = SamplingConfiguration.from_frequency_division(int(ptr.freq_div))
            Base().modulation_calc_get_result(res, buf.ctypes.data_as(POINTER(c_uint8)))  # type: ignore[arg-type]
            self._cache = np.fromiter((EmitIntensity(int(x)) for x in buf), dtype=EmitIntensity)
        return self._cache

    def calc(self: "Cache[M]") -> np.ndarray:
        """Calculate modulation."""
        return self._init()

    def _modulation_ptr(self: "Cache[M]") -> ModulationPtr:
        data = np.fromiter((m.value for m in self.calc()), dtype=c_uint8)
        size = len(data)
        return Base().modulation_custom(
            self._sampling_config._internal,  # type: ignore[union-attr]
            data.ctypes.data_as(POINTER(c_uint8)),  # type: ignore[arg-type]
            size,
            self._loop_behavior._internal,
        )

    @property
    def buffer(self: "Cache[M]") -> np.ndarray | None:
        """Get cached data."""
        return self._cache


class IntoModulationCache(ModulationBase[M], Generic[M]):
    """Modulation interface of Cache."""

    def with_cache(self: M) -> "Cache[M]":
        """Cache the result of calculation."""
        return Cache(self)
