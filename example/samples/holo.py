import numpy as np

from pyautd3 import Controller, Hz, Silencer, Sine, SineOption
from pyautd3.gain.holo import GSPAT, GSPATOption, NalgebraBackend, Pa


def holo(autd: Controller) -> None:
    config = Silencer()
    autd.send(config)

    center = autd.center + np.array([0.0, 0.0, 150.0])
    backend = NalgebraBackend()
    f = GSPAT(
        backend=backend,
        foci=[(center - np.array([30.0, 0.0, 0.0]), 10e3 * Pa), (center + np.array([30.0, 0.0, 0.0]), 10e3 * Pa)],
        option=GSPATOption(),
    )
    m = Sine(freq=150 * Hz, option=SineOption())

    autd.send((m, f))
