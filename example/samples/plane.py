import numpy as np

from pyautd3 import ConfigureSilencer, Controller
from pyautd3.gain import Plane
from pyautd3.modulation import Sine


async def plane(autd: Controller) -> None:
    config = ConfigureSilencer.default()
    await autd.send_async(config)

    f = Plane(np.array([0.0, 0.0, 1.0]))
    m = Sine(150)

    await autd.send_async(m, f)
