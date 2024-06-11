import numpy as np

from pyautd3 import Controller, Hz, Plane, Silencer, Sine


def plane(autd: Controller) -> None:
    config = Silencer.default()
    autd.send(config)

    f = Plane(np.array([0.0, 0.0, 1.0]))
    m = Sine(150 * Hz)

    autd.send((m, f))
