import numpy as np

from pyautd3 import ConfigureSilencer, Controller, Focus, FocusSTM, GainSTM, Static


async def stm_focus(autd: Controller) -> None:
    config = ConfigureSilencer.disable()
    await autd.send_async(config)

    m = Static()

    radius = 30.0
    size = 200
    center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
    stm = FocusSTM.from_freq(1.0).add_foci_from_iter(
        center + radius * np.array([np.cos(theta), np.sin(theta), 0]) for theta in (2.0 * np.pi * i / size for i in range(size))
    )

    await autd.send_async(m, stm)


async def stm_gain(autd: Controller) -> None:
    config = ConfigureSilencer.disable()
    await autd.send_async(config)

    m = Static()

    radius = 30.0
    size = 50
    center = autd.geometry.center + np.array([0.0, 0.0, 150.0])
    stm = GainSTM.from_freq(1.0).add_gains_from_iter(
        Focus(center + radius * np.array([np.cos(theta), np.sin(theta), 0])) for theta in (2.0 * np.pi * i / size for i in range(size))
    )

    await autd.send_async(m, stm)
