import numpy as np

from pyautd3 import Bessel, BesselOption, Controller, Hz, Silencer, Sine, SineOption, rad


def bessel(autd: Controller) -> None:
    config = Silencer()
    autd.send(config)

    f = Bessel(pos=autd.center(), direction=np.array([0.0, 0.0, 1.0]), theta=13.0 / 180 * np.pi * rad, option=BesselOption())
    m = Sine(freq=150 * Hz, option=SineOption())

    autd.send((m, f))
