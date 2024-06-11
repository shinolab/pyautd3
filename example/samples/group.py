import numpy as np

from pyautd3 import Controller, Device, Focus, Group, Hz, Null, Silencer, Sine, Static


def group_by_device(autd: Controller) -> None:
    config = Silencer.default()
    autd.send(config)

    def grouping(dev: Device) -> str | None:
        match dev.idx:
            case 0:
                return "null"
            case 1:
                return "focus"
            case _:
                return None

    autd.group(grouping).set("null", (Static(), Null())).set(
        "focus",
        (Sine(150 * Hz), Focus(autd.geometry.center + np.array([0.0, 0.0, 150.0]))),
    ).send()


def group_by_transducer(autd: Controller) -> None:
    config = Silencer.default()
    autd.send(config)

    cx = autd.geometry.center[0]
    g1 = Focus(autd.geometry.center + np.array([0, 0, 150]))
    g2 = Null()

    g = Group(lambda _: lambda tr: "focus" if tr.position[0] < cx else "null").set("focus", g1).set("null", g2)

    m = Sine(150 * Hz)

    autd.send((m, g))
