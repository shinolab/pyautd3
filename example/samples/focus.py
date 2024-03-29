import numpy as np

from pyautd3 import ConfigureSilencer, Controller, Focus, Sine


async def simple(autd: Controller) -> None:
    config = ConfigureSilencer.default()
    await autd.send_async(config)

    f = Focus(autd.geometry.center + np.array([0.0, 0.0, 150.0]))
    m = Sine(150)

    await autd.send_async(m, f)
