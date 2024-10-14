from typing import Generic, TypeVar

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

M = TypeVar("M", bound=ModulationBase)


class Cache(ModulationBase["Cache[M]"], Generic[M]):
    _m: M
    _ptr: ModulationPtr | None

    def __init__(self: "Cache", m: M) -> None:
        super().__init__()
        self._m = m
        self._ptr = None
        self._loop_behavior = m.loop_behavior

    def _modulation_ptr(self: "Cache[M]") -> ModulationPtr:
        if self._ptr is None:
            self._ptr = Base().modulation_cache(self._m._modulation_ptr())
        return Base().modulation_cache_clone(self._ptr, self._loop_behavior)

    def __del__(self: "Cache[M]") -> None:
        if self._ptr is not None:
            Base().modulation_cache_free(self._ptr)


class IntoModulationCache(ModulationBase[M], Generic[M]):
    def with_cache(self: M) -> "Cache[M]":
        return Cache(self)
