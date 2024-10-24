from collections.abc import Iterable
from typing import Generic, Self, TypeVar

import numpy as np

from pyautd3.driver.datagram.gain import Gain
from pyautd3.native_methods.autd3capi_gain_holo import EmissionConstraintWrap

from .amplitude import Amplitude
from .backend import Backend

H = TypeVar("H", bound="Holo")


class Holo(Gain[H], Generic[H]):
    _foci: list[np.ndarray]
    _amps: list[Amplitude]
    _constraint: EmissionConstraintWrap

    def __init__(self: Self, constraint: EmissionConstraintWrap, iterable: Iterable[tuple[np.ndarray, Amplitude]]) -> None:
        foci = list(iterable)
        self._foci = [np.array(focus) for focus, _ in foci]
        self._amps = [amp for _, amp in foci]
        self._constraint = constraint

    def with_constraint(self: H, constraint: EmissionConstraintWrap) -> H:
        self._constraint = constraint
        return self


class HoloWithBackend(Holo[H], Generic[H]):
    _backend: Backend

    def __init__(
        self: Self,
        constraint: EmissionConstraintWrap,
        backend: Backend,
        iterable: Iterable[tuple[np.ndarray, Amplitude]],
    ) -> None:
        super().__init__(constraint, iterable)
        self._backend = backend
