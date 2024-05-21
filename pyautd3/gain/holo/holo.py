import functools
from collections.abc import Iterable
from typing import Generic, TypeVar

import numpy as np
from numpy.typing import ArrayLike

from pyautd3.driver.datagram.gain import Gain
from pyautd3.native_methods.autd3capi_gain_holo import EmissionConstraintWrap

from .amplitude import Amplitude
from .backend import Backend

H = TypeVar("H", bound="Holo")


class Holo(Gain[H], Generic[H]):
    _foci: list[float]
    _amps: list[Amplitude]
    _constraint: EmissionConstraintWrap

    def __init__(self: "Holo", constraint: EmissionConstraintWrap) -> None:
        self._foci = []
        self._amps = []
        self._constraint = constraint

    def add_focus(self: H, focus: ArrayLike, amp: Amplitude) -> H:
        focus = np.array(focus)
        self._foci.append(focus[0])
        self._foci.append(focus[1])
        self._foci.append(focus[2])
        self._amps.append(amp)
        return self

    def add_foci_from_iter(self: H, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> H:
        return functools.reduce(
            lambda acc, x: acc.add_focus(x[0], x[1]),
            iterable,
            self,
        )

    def with_constraint(self: H, constraint: EmissionConstraintWrap) -> H:
        self._constraint = constraint
        return self


class HoloWithBackend(Holo[H], Generic[H]):
    _backend: Backend

    def __init__(self: "HoloWithBackend", constraint: EmissionConstraintWrap, backend: Backend) -> None:
        super().__init__(constraint)
        self._backend = backend
