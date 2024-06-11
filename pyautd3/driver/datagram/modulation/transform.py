import ctypes
from collections.abc import Callable
from typing import Generic, TypeVar

from pyautd3.driver.geometry.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

from .base import ModulationBase
from .cache import IntoModulationCache
from .radiation_pressure import IntoModulationRadiationPressure

M = TypeVar("M", bound="ModulationBase")


class Transform(
    IntoModulationCache["Transform[M]"],
    IntoModulationRadiationPressure["Transform[M]"],
    ModulationBase["Transform[M]"],
    Generic[M],
):
    _m: M

    def __init__(self: "Transform[M]", m: M, f: Callable[[int, int], int]) -> None:
        self._m = m
        self._loop_behavior = m._loop_behavior
        self._f_native = ctypes.CFUNCTYPE(ctypes.c_uint8, ctypes.c_void_p, ctypes.c_uint16, ctypes.c_uint8)(
            lambda _, i, d: f(int(i), int(d)),
        )

    def _modulation_ptr(self: "Transform[M]", geometry: Geometry) -> ModulationPtr:
        return Base().modulation_with_transform(
            self._m._modulation_ptr(geometry),
            self._f_native,  # type: ignore[arg-type]
            None,
            self._loop_behavior,
        )


class IntoModulationTransform(ModulationBase[M], Generic[M]):
    def with_transform(self: M, f: Callable[[int, int], int]) -> "Transform[M]":
        return Transform(self, f)
