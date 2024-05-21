from pathlib import Path

import numpy as np

from pyautd3 import Controller, Focus, Silencer
from pyautd3.modulation.audio_file import Wav


def wav(autd: Controller) -> None:
    config = Silencer.default()
    autd.send(config)

    f = Focus(autd.geometry.center + np.array([0.0, 0.0, 150.0]))
    m = Wav(Path(__file__).parent / "sin150.wav")

    autd.send((m, f))
