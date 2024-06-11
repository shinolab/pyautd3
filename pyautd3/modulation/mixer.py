from collections.abc import Iterable

import numpy as np

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.modulation.cache import IntoModulationCache
from pyautd3.driver.datagram.modulation.radiation_pressure import IntoModulationRadiationPressure
from pyautd3.driver.datagram.modulation.transform import IntoModulationTransform
from pyautd3.driver.geometry.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import ModulationPtr

from .sine import Sine


class Mixer(
    IntoModulationCache["Mixer"],
    IntoModulationRadiationPressure["Mixer"],
    IntoModulationTransform["Mixer"],
    ModulationBase["Mixer"],
):
    _components: list[Sine]

    def __init__(self: "Mixer", iterable: Iterable[Sine]) -> None:
        super().__init__()
        self._components = list(iterable)

    def _modulation_ptr(self: "Mixer", geometry: Geometry) -> ModulationPtr:
        components: np.ndarray = np.ndarray(len(self._components), dtype=ModulationPtr)
        for i, m in enumerate(self._components):
            components[i]["_0"] = m._modulation_ptr(geometry)._0
        return self._components[0]._mode.mixer_ptr(
            components,
            len(self._components),
            self._loop_behavior,
        )
