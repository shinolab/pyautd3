from collections.abc import Iterable
from typing import Self

from pyautd3.derive.builder import builder
from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.fir import IntoModulationFir
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

from .sine import Sine


@builder
class Fourier(
    IntoModulationCache["Fourier"],
    IntoModulationFir["Fourier"],
    IntoModulationRadiationPressure["Fourier"],
    ModulationBase["Fourier"],
):
    _components: list[Sine]
    _param_clamp: bool
    _param_scale_factor: float | None
    _param_offset: int

    def __init__(self: Self, iterable: Iterable[Sine]) -> None:
        super().__init__()
        self._components = list(iterable)
        self._param_clamp = False
        self._param_scale_factor = float("nan")
        self._param_offset = 0

    def _modulation_ptr(self: Self) -> ModulationPtr:
        return self._components[0]._mode.fourier_ptr(
            self._components,
            len(self._components),
            self._param_clamp,
            self._param_scale_factor if self._param_scale_factor is not None else float("nan"),  # type: ignore[arg-type]
            self._param_offset,
            self._loop_behavior,
        )
