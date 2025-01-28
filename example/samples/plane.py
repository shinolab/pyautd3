import numpy as np

from pyautd3 import Controller, Hz, Plane, PlaneOption, Silencer, Sine, SineOption


def plane(autd: Controller) -> None:
    config = Silencer()
    autd.send(config)

    f = Plane(direction=np.array([0.0, 0.0, 1.0]), option=PlaneOption())
    m = Sine(freq=150 * Hz, option=SineOption())

    autd.send((m, f))
