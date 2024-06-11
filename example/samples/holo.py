import numpy as np

from pyautd3 import Controller, Hz, Silencer, Sine
from pyautd3.gain.holo import GSPAT, NalgebraBackend, Pa


def holo(autd: Controller) -> None:
    config = Silencer.default()
    autd.send(config)

    center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
    backend = NalgebraBackend()
    f = GSPAT(backend, [(center - np.array([30.0, 0.0, 0.0]), 10e3 * Pa), (center + np.array([30.0, 0.0, 0.0]), 10e3 * Pa)])
    m = Sine(150 * Hz)

    autd.send((m, f))
