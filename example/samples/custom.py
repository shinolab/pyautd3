from collections.abc import Callable

from pyautd3 import Controller, Device, Drive, EmitIntensity, Hz, Phase, Silencer, Sine, SineOption, Transducer
from pyautd3.gain import Custom


def custom(autd: Controller) -> None:
    config = Silencer()
    autd.send(config)

    def f(dev: Device) -> Callable[[Transducer], Drive]:
        return lambda tr: Drive(phase=Phase(0), intensity=EmitIntensity.MAX) if dev.idx() == 0 and tr.idx() in (0, 248) else Drive.NULL

    g = Custom(f)
    m = Sine(freq=150 * Hz, option=SineOption())

    autd.send((m, g))
