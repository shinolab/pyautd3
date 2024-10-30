from collections.abc import Iterable
from typing import Self

from pyautd3.derive import builder, datagram, modulation
from pyautd3.derive.derive_datagram import datagram_with_segment
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.modulation.sine import Sine
from pyautd3.native_methods.autd3capi_driver import ModulationPtr


@modulation
@datagram
@datagram_with_segment
@builder
class Fourier(Modulation):
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
