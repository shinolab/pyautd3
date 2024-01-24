import numpy as np

from pyautd3 import ConfigureSilencer, Controller, Sine
from pyautd3.gain.holo import GSPAT, NalgebraBackend, pascal


async def holo(autd: Controller) -> None:
    config = ConfigureSilencer.default()
    await autd.send_async(config)

    center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
    backend = NalgebraBackend()
    f = GSPAT(backend).add_focus(center - np.array([30.0, 0.0, 0.0]), 10e3 * pascal).add_focus(center + np.array([30.0, 0.0, 0.0]), 10e3 * pascal)
    m = Sine(150)

    await autd.send_async(m, f)
