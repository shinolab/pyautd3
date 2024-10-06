from collections.abc import Iterable

import numpy as np

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

    def __init__(self: "Fourier", iterable: Iterable[Sine]) -> None:
        super().__init__()
        self._components = list(iterable)
        self._clamp = False
        self._scale_factor = float("nan")

    def with_clamp(self: "Fourier", clamp: bool) -> "Fourier":  # noqa: FBT001
        self._clamp = clamp
        return self

    @property
    def clamp(self: "Fourier") -> bool:
        return self._clamp

    def with_scale_factor(self: "Fourier", scale_factor: float | None) -> "Fourier":
        self._scale_factor = scale_factor
        return self

    @property
    def scale_factor(self: "Fourier") -> float | None:
        return self._scale_factor

    def _modulation_ptr(self: "Fourier") -> ModulationPtr:
        components: np.ndarray = np.ndarray(len(self._components), dtype=ModulationPtr)
        for i, m in enumerate(self._components):
            components[i]["_0"] = m._modulation_ptr()._0
        return self._components[0]._mode.fourier_ptr(
            components,
            len(self._components),
            self._clamp,
            self._scale_factor if self.scale_factor is not None else float("nan"),  # type: ignore[arg-type]
            self._loop_behavior,
        )
