import os

from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller, Nop, tracing_init

if __name__ == "__main__":
    os.environ["RUST_LOG"] = "autd3=TRACE"

    tracing_init()

    with Controller.open([AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])], Nop()) as autd:
        runner.run(autd)
