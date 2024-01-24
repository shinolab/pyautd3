import functools
from collections.abc import Iterable
from functools import reduce

from pyautd3.driver.datagram.modulation import IModulation
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import ModulationPtr

from .sine import Sine


class Fourier(IModulation):
    """Multi-frequency sine wave modulation."""

    _components: list[Sine]

    def __init__(self: "Fourier", sine: Sine) -> None:
        super().__init__()
        self._components = [sine]

    def add_component(self: "Fourier", component: Sine) -> "Fourier":
        """Add a sine wave component.

        Arguments:
        ---------
            component: `Sine` modulation
        """
        self._components.append(component)
        return self

    def add_components_from_iter(self: "Fourier", components: Iterable[Sine]) -> "Fourier":
        """Add sine wave components from iterable.

        Arguments:
        ---------
            components: Iterable of `Sine` modulations
        """
        return functools.reduce(lambda acc, x: acc.add_component(x), components, self)

    def __add__(self: "Fourier", rhs: Sine) -> "Fourier":
        """Add a sine wave component.

        Arguments:
        ---------
            rhs: `Sine` modulation
        """
        return self.add_component(rhs)

    def _modulation_ptr(self: "Fourier") -> ModulationPtr:
        return reduce(
            lambda acc, s: Base().modulation_fourier_add_component(acc, s._modulation_ptr()),
            self._components[1:],
            Base().modulation_fourier(self._components[0]._modulation_ptr()),
        )
