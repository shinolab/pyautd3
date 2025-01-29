from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller
from pyautd3.link.twincat import TwinCAT

if __name__ == "__main__":
    with Controller.open([AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])], TwinCAT()) as autd:
        runner.run(autd)
