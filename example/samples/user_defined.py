import numpy as np
from numpy.typing import ArrayLike

from pyautd3 import Controller, Drive, EmitIntensity, Geometry, Hz, Phase, SamplingConfig, Silencer, rad
from pyautd3.gain import Gain
from pyautd3.modulation import Modulation
from pyautd3.native_methods.autd3capi_driver import SamplingConfigWrap


class Focus(Gain["Focus"]):
    def __init__(self: "Focus", point: ArrayLike) -> None:
        self.point = np.array(point)

    def calc(self: "Focus", geometry: Geometry) -> dict[int, np.ndarray]:
        return Gain._transform(
            geometry,
            lambda dev: lambda tr: Drive(
                Phase(float(np.linalg.norm(tr.position - self.point)) * dev.wavenumber * rad),
                EmitIntensity.maximum(),
            ),
        )


class Burst(Modulation["Burst"]):
    _length: int

    def __init__(self: "Burst", length: int, config: SamplingConfigWrap | None = None) -> None:
        super().__init__(config if config is not None else SamplingConfig.Freq(4000 * Hz))
        self._length = length

    def calc(self: "Burst", _: Geometry) -> np.ndarray:
        buf = np.array([EmitIntensity.minimum()] * self._length)
        buf[0] = EmitIntensity.maximum()
        return buf


def user_defined(autd: Controller) -> None:
    config = Silencer.default()
    autd.send(config)

    f = Focus(autd.geometry.center + np.array([0.0, 0.0, 150.0]))
    m = Burst(4000)

    autd.send(m, f)
