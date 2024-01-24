import numpy as np

from pyautd3 import ConfigureSilencer, Controller
from pyautd3.gain import Bessel
from pyautd3.modulation import Sine


async def bessel(autd: Controller) -> None:
    config = ConfigureSilencer.default()
    await autd.send_async(config)

    f = Bessel(autd.geometry.center, np.array([0.0, 0.0, 1.0]), 13.0 / 180 * np.pi)
    m = Sine(150)

    await autd.send_async(m, f)
