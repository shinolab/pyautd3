import functools
from collections.abc import Iterable
from typing import Generic, TypeVar

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.gain import Gain

from .amplitude import Amplitude
from .backend import Backend
from .constraint import EmissionConstraint, IEmissionConstraint

__all__ = ["EmissionConstraint"]


H = TypeVar("H", bound="Holo")


class Holo(Gain[H], Generic[H]):
    _foci: list[float]
    _amps: list[Amplitude]
    _constraint: IEmissionConstraint

    def __init__(self: "Holo", constraint: IEmissionConstraint) -> None:
        self._foci = []
        self._amps = []
        self._constraint = constraint

    def add_focus(self: H, focus: ArrayLike, amp: Amplitude) -> H:
        """Add focus.

        Arguments:
        ---------
            focus: Focus point
            amp: Focus amplitude

        """
        focus = np.array(focus)
        self._foci.append(focus[0])
        self._foci.append(focus[1])
        self._foci.append(focus[2])
        self._amps.append(amp)
        return self

    def add_foci_from_iter(self: H, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> H:
        """Add foci from iterable.

        Arguments:
        ---------
            iterable: Iterable of focus point and amplitude.

        """
        return functools.reduce(
            lambda acc, x: acc.add_focus(x[0], x[1]),
            iterable,
            self,
        )

    def with_constraint(self: H, constraint: IEmissionConstraint) -> H:
        """Set amplitude constraint.

        Arguments:
        ---------
            constraint: Amplitude constraint

        """
        self._constraint = constraint
        return self

    @property
    def constraint(self: H) -> IEmissionConstraint:
        """Get emission constraint."""
        return self._constraint


class HoloWithBackend(Holo[H], Generic[H]):
    _backend: Backend

    def __init__(self: "HoloWithBackend", constraint: IEmissionConstraint, backend: Backend) -> None:
        super().__init__(constraint)
        self._backend = backend
