from pathlib import Path

import numpy as np

from pyautd3 import ConfigureSilencer, Controller
from pyautd3.gain import Focus
from pyautd3.modulation.audio_file import Wav


async def wav(autd: Controller) -> None:
    config = ConfigureSilencer.default()
    await autd.send_async(config)

    f = Focus(autd.geometry.center + np.array([0.0, 0.0, 150.0]))
    m = Wav(Path(__file__).parent / "sin150.wav")

    await autd.send_async((m, f))
