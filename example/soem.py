import os

from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller, tracing_init
from pyautd3.link.soem import SOEM, Status


def err_handler(slave: int, status: Status) -> None:
    print(f"slave[{slave}]: {status}")
    if status == Status.Lost():
        # You can also wait for the link to recover, without exitting the process
        os._exit(-1)


if __name__ == "__main__":
    os.environ["RUST_LOG"] = "autd3=INFO"

    tracing_init()

    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(
        SOEM.builder().with_err_handler(err_handler),
    ) as autd:
        runner.run(autd)
