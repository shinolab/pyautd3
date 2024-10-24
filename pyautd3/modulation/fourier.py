from collections.abc import Iterable
from typing import Self

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.fir import IntoModulationFir
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

from .sine import Sine


class Fourier(
    IntoModulationCache["Fourier"],
    IntoModulationFir["Fourier"],
    IntoModulationRadiationPressure["Fourier"],
    ModulationBase["Fourier"],
):
    _components: list[Sine]
    _clamp: bool
    _scale_factor: float | None
    _offset: int

    def __init__(self: Self, iterable: Iterable[Sine]) -> None:
        super().__init__()
        self._components = list(iterable)
        self._clamp = False
        self._scale_factor = float("nan")
        self._offset = 0

    def with_clamp(self: Self, clamp: bool) -> Self:  # noqa: FBT001
        self._clamp = clamp
        return self

    @property
    def clamp(self: Self) -> bool:
        return self._clamp

    def with_scale_factor(self: Self, scale_factor: float | None) -> Self:
        self._scale_factor = scale_factor
        return self

    @property
    def scale_factor(self: Self) -> float | None:
        return self._scale_factor

    def with_offset(self: Self, offset: int) -> Self:
        self._offset = offset
        return self

    @property
    def offset(self: Self) -> int:
        return self._offset

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return self._components[0]._mode.fourier_ptr(
            self._components,
            len(self._components),
            self._clamp,
            self._scale_factor if self._scale_factor is not None else float("nan"),  # type: ignore[arg-type]
            self._offset,
            self._loop_behavior,
        )
