from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller
from pyautd3.link.simulator import Simulator

if __name__ == "__main__":
    with Controller[Simulator].open(
        [AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0]), AUTD3(pos=[AUTD3.DEVICE_WIDTH, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])],
        Simulator("127.0.0.1:8080"),
    ) as autd:
        runner.run(autd)
