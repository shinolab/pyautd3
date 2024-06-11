import numpy as np

from pyautd3 import Controller, Focus, Hz, Silencer, Sine


def simple(autd: Controller) -> None:
    config = Silencer.default()
    autd.send(config)

    f = Focus(autd.geometry.center + np.array([0.0, 0.0, 150.0]))
    m = Sine(150 * Hz)

    autd.send((m, f))
