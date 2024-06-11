from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller
from pyautd3.link.soem import RemoteSOEM

if __name__ == "__main__":
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(
        RemoteSOEM.builder("127.0.0.1:8080"),
    ) as autd:
        runner.run(autd)
