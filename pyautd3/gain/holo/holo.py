import functools
from collections.abc import Iterable
from typing import TypeVar

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.gain.gain import IGain

from .amplitude import Amplitude
from .backend import Backend
from .constraint import EmissionConstraint

__all__ = []  # type: ignore[var-annotated]


H = TypeVar("H", bound="Holo")


class Holo(IGain):
    _foci: list[float]
    _amps: list[Amplitude]
    _constraint: EmissionConstraint

    def __init__(self: "Holo", constraint: EmissionConstraint) -> None:
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

    def with_constraint(self: H, constraint: EmissionConstraint) -> H:
        """Set amplitude constraint.

        Arguments:
        ---------
            constraint: Amplitude constraint
        """
        self._constraint = constraint
        return self

    def constraint(self: H) -> EmissionConstraint:
        """Get emission constraint."""
        return self._constraint


class HoloWithBackend(Holo):
    _backend: Backend

    def __init__(self: "HoloWithBackend", constraint: EmissionConstraint, backend: Backend) -> None:
        super().__init__(constraint)
        self._backend = backend
