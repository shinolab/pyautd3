from collections.abc import Iterable
from typing import Generic, Self, TypeVar

import numpy as np

from pyautd3.driver.datagram.gain import Gain
from pyautd3.gain.holo.backend import Backend

from .amplitude import Amplitude

H = TypeVar("H", bound="Holo")


class Holo(Gain, Generic[H]):
    foci: list[tuple[np.ndarray, Amplitude]]

    def __init__(self: Self, foci: Iterable[tuple[np.ndarray, Amplitude]]) -> None:
        self.foci = list(foci)


class HoloWithBackend(Holo[H], Generic[H]):
    backend: Backend

    def __init__(
        self: Self,
        foci: Iterable[tuple[np.ndarray, Amplitude]],
        backend: Backend,
    ) -> None:
        super().__init__(foci)
        self.backend = backend
