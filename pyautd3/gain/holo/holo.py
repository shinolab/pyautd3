from collections.abc import Iterable
from typing import Self, TypeVar

import numpy as np

from pyautd3.driver.datagram.gain import Gain

from .amplitude import Amplitude

H = TypeVar("H", bound="Holo")


class Holo[H: "Holo"](Gain):
    foci: list[tuple[np.ndarray, Amplitude]]

    def __init__(self: Self, foci: Iterable[tuple[np.ndarray, Amplitude]]) -> None:
        self.foci = list(foci)
