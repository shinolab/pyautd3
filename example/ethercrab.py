import os

from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller
from pyautd3.link.ethercrab import EtherCrab, EtherCrabOption, Status, tracing_init


def err_handler(slave: int, status: Status) -> None:
    print(f"slave[{slave}]: {status}")


if __name__ == "__main__":
    os.environ["RUST_LOG"] = "autd3=INFO"

    tracing_init()

    with Controller.open([AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])], EtherCrab(err_handler, EtherCrabOption())) as autd:
        runner.run(autd)
