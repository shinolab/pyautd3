from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller
from pyautd3.link.twincat import TwinCAT

if __name__ == "__main__":
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(TwinCAT.builder()) as autd:
        runner.run(autd)
