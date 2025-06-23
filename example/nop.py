from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller, Nop

if __name__ == "__main__":
    with Controller.open([AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])], Nop()) as autd:
        runner.run(autd)
