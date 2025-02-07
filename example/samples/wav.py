from pathlib import Path

import numpy as np

from pyautd3 import Controller, Focus, FocusOption, Silencer
from pyautd3.modulation.audio_file import Wav


def wav(autd: Controller) -> None:
    config = Silencer()
    autd.send(config)

    f = Focus(pos=autd.center() + np.array([0.0, 0.0, 150.0]), option=FocusOption())
    m = Wav(path=Path(__file__).parent / "sin150.wav")

    autd.send((m, f))
