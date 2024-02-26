import ctypes
from collections.abc import Callable
from typing import Generic, TypeVar

from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import ModulationPtr

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
    """Modulation to transform modulation data."""

    _m: M

    def __init__(self: "Transform[M]", m: M, f: Callable[[int, EmitIntensity], EmitIntensity]) -> None:
        self._m = m
        self._loop_behavior = m._loop_behavior
        self._f_native = ctypes.CFUNCTYPE(ctypes.c_uint8, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint8)(
            lambda _, i, d: f(
                int(i),
                EmitIntensity(d),
            ).value,
        )

    def _modulation_ptr(self: "Transform[M]") -> ModulationPtr:
        return Base().modulation_with_transform(
            self._m._modulation_ptr(),
            self._f_native,  # type: ignore[arg-type]
            None,
            self._loop_behavior._internal,
        )


class IntoModulationTransform(ModulationBase[M], Generic[M]):
    """Modulation interface of Transform."""

    def with_transform(self: M, f: Callable[[int, EmitIntensity], EmitIntensity]) -> "Transform[M]":
        """Transform modulation data.

        Arguments:
        ---------
            self: Modulation
            f: Transform function. The first argument is the index of the modulation data, and the second is the original data.

        """
        return Transform(self, f)
