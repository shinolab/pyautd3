import numpy as np

from pyautd3 import Controller, Device, Focus, FocusOption, Group, Hz, Null, Silencer, Sine, SineOption, Static


def group_by_device(autd: Controller) -> None:
    config = Silencer()
    autd.send(config)

    def key_map(dev: Device) -> str | None:
        match dev.idx:
            case 0:
                return "null"
            case 1:
                return "focus"
            case _:
                return None

    autd.group_send(
        key_map,
        {
            "null": (Static(), Null()),
            "focus": (Sine(freq=150 * Hz, option=SineOption()), Focus(pos=autd.center() + np.array([0.0, 0.0, 150.0]), option=FocusOption())),
        },
    )


def group_by_transducer(autd: Controller) -> None:
    config = Silencer()
    autd.send(config)

    cx = autd.center()[0]
    g1 = Focus(pos=autd.center() + np.array([0, 0, 150]), option=FocusOption())
    g2 = Null()

    g = Group(key_map=lambda _: lambda tr: "focus" if tr.position()[0] < cx else "null", gain_map={"focus": g1, "null": g2})

    m = Sine(freq=150 * Hz, option=SineOption())

    autd.send((m, g))
