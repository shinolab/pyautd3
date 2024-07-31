from collections.abc import Callable

from pyautd3 import Controller, Device, Drive, EmitIntensity, Hz, Phase, Silencer, Sine, Transducer
from pyautd3.gain import Custom


def transtest(autd: Controller) -> None:
    config = Silencer.default()
    autd.send(config)

    def f(dev: Device) -> Callable[[Transducer], Drive]:
        return lambda tr: Drive((Phase(0), EmitIntensity.maximum())) if dev.idx == 0 and tr.idx in (0, 248) else Drive.null()

    g = Custom(f)
    m = Sine(150 * Hz)

    autd.send((m, g))
