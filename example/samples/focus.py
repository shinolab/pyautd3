import numpy as np

from pyautd3 import Controller, Focus, FocusOption, Hz, Silencer, Sine, SineOption


def simple(autd: Controller) -> None:
    config = Silencer()
    autd.send(config)

    f = Focus(pos=autd.center() + np.array([0.0, 0.0, 150.0]), option=FocusOption())
    m = Sine(freq=150 * Hz, option=SineOption())

    autd.send((m, f))
