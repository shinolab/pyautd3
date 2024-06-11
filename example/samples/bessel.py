import numpy as np

from pyautd3 import Bessel, Controller, Hz, Silencer, Sine, rad


def bessel(autd: Controller) -> None:
    config = Silencer.default()
    autd.send(config)

    f = Bessel(autd.geometry.center, np.array([0.0, 0.0, 1.0]), 13.0 / 180 * np.pi * rad)
    m = Sine(150 * Hz)

    autd.send((m, f))
