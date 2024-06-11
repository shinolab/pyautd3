from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller
from pyautd3.link.simulator import Simulator

if __name__ == "__main__":
    with (
        Controller[Simulator]
        .builder([AUTD3([0.0, 0.0, 0.0]), AUTD3([AUTD3.DEVICE_WIDTH, 0.0, 0.0])])
        .open(
            Simulator.builder(8080),
        ) as autd
    ):
        runner.run(autd)
