from pyautd3 import ConfigureSilencer, Controller, Device, Drive, EmitIntensity, Phase, Sine, Transducer, TransducerTest


async def transtest(autd: Controller) -> None:
    config = ConfigureSilencer.default()
    await autd.send_async(config)

    def f(dev: Device, tr: Transducer) -> Drive | None:
        match (dev.idx, tr.idx):
            case (0, 0):
                return Drive(Phase(0), EmitIntensity.maximum())
            case (0, 248):
                return Drive(Phase(0), EmitIntensity.maximum())
            case _:
                return None

    g = TransducerTest(f)
    m = Sine(150)

    await autd.send_async(m, g)
