import numpy as np
from numpy.typing import ArrayLike

from pyautd3 import ConfigureSilencer, Controller, Drive, EmitIntensity, Geometry, Phase, SamplingConfiguration
from pyautd3.gain import Gain
from pyautd3.modulation import Modulation


class Focus(Gain["Focus"]):
    def __init__(self: "Focus", point: ArrayLike) -> None:
        self.point = np.array(point)

    def calc(self: "Focus", geometry: Geometry) -> dict[int, np.ndarray]:
        return Gain._transform(
            geometry,
            lambda dev, tr: Drive(
                Phase.from_rad(float(np.linalg.norm(tr.position - self.point)) * tr.wavenumber(dev.sound_speed)),
                EmitIntensity.maximum(),
            ),
        )


class Burst(Modulation["Burst"]):
    _length: int

    def __init__(self: "Burst", length: int, config: SamplingConfiguration | None = None) -> None:
        super().__init__(config if config is not None else SamplingConfiguration.from_frequency(4e3))
        self._length = length

    def calc(self: "Burst") -> np.ndarray:
        buf = np.array([EmitIntensity.minimum()] * self._length)
        buf[0] = EmitIntensity.maximum()
        return buf


async def custom(autd: Controller) -> None:
    config = ConfigureSilencer.default()
    await autd.send_async(config)

    f = Focus(autd.geometry.center + np.array([0.0, 0.0, 150.0]))
    m = Burst(4000)

    await autd.send_async(m, f)
