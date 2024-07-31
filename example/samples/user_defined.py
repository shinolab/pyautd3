from collections.abc import Callable
from datetime import timedelta

import numpy as np
from numpy.typing import ArrayLike

from pyautd3 import Controller, Device, Drive, EmitIntensity, Geometry, Hz, Phase, SamplingConfig, Silencer, Transducer, rad
from pyautd3.driver.defined.freq import Freq
from pyautd3.gain import Gain
from pyautd3.modulation import Modulation


class Focus(Gain["Focus"]):
    def __init__(self: "Focus", point: ArrayLike) -> None:
        self.point = np.array(point)

    def calc(self: "Focus", _: Geometry) -> Callable[[Device], Callable[[Transducer], Drive | EmitIntensity | Phase | tuple]]:
        return Gain._transform(
            lambda dev: lambda tr: Drive(
                (Phase(float(np.linalg.norm(tr.position - self.point)) * dev.wavenumber * rad), EmitIntensity.maximum()),
            ),
        )


class Burst(Modulation["Burst"]):
    _length: int

    def __init__(self: "Burst", length: int, config: SamplingConfig | Freq[int] | timedelta | None = None) -> None:
        super().__init__(config if config is not None else 4000 * Hz)
        self._length = length

    def calc(self: "Burst") -> np.ndarray:
        buf = np.array([EmitIntensity.minimum()] * self._length)
        buf[0] = EmitIntensity.maximum()
        return buf


def user_defined(autd: Controller) -> None:
    config = Silencer.default()
    autd.send(config)

    f = Focus(autd.geometry.center + np.array([0.0, 0.0, 150.0]))
    m = Burst(4000)

    autd.send((m, f))
