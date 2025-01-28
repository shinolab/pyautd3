import numpy as np

from pyautd3 import Controller, FociSTM, Focus, FocusOption, GainSTM, GainSTMOption, Hz, Silencer, Static


def stm_focus(autd: Controller) -> None:
    config = Silencer.disable()
    autd.send(config)

    m = Static()

    radius = 30.0
    size = 200
    center = autd.center + np.array([0.0, 0.0, 150.0])
    stm = FociSTM(
        foci=(center + radius * np.array([np.cos(theta), np.sin(theta), 0]) for theta in (2.0 * np.pi * i / size for i in range(size))),
        config=1.0 * Hz,
    )

    autd.send((m, stm))


def stm_gain(autd: Controller) -> None:
    config = Silencer.disable()
    autd.send(config)

    m = Static()

    radius = 30.0
    size = 50
    center = autd.center + np.array([0.0, 0.0, 150.0])
    stm = GainSTM(
        gains=(
            Focus(pos=center + radius * np.array([np.cos(theta), np.sin(theta), 0]), option=FocusOption())
            for theta in (2.0 * np.pi * i / size for i in range(size))
        ),
        config=1.0 * Hz,
        option=GainSTMOption(),
    )

    autd.send((m, stm))
