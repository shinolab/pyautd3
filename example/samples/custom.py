from pyautd3 import Controller, Device, Drive, EmitIntensity, Hz, Phase, Silencer, Sine, Transducer
from pyautd3.gain import Custom


def transtest(autd: Controller) -> None:
    config = Silencer.default()
    autd.send(config)

    def f(dev: Device, tr: Transducer) -> Drive:
        match (dev.idx, tr.idx):
            case (0, 0):
                return Drive(Phase(0), EmitIntensity.maximum())
            case (0, 248):
                return Drive(Phase(0), EmitIntensity.maximum())
            case _:
                return Drive.null()

    g = Custom(f)
    m = Sine(150 * Hz)

    autd.send(m, g)
