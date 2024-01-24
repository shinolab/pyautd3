"""
File: simulator.py
Project: example
Created Date: 29/08/2023
Author: Shun Suzuki
-----
Last Modified: 23/01/2024
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2023 Shun Suzuki. All rights reserved.

"""

import asyncio

from samples import runner  # type: ignore[import,import-not-found]

from pyautd3 import AUTD3, Controller
from pyautd3.link.simulator import Simulator


async def main() -> None:
    async with (
        Controller[Simulator]
        .builder()
        .add_device(AUTD3([0.0, 0.0, 0.0]))
        .add_device(AUTD3([AUTD3.device_width(), 0.0, 0.0]))
        .open_with_async(
            Simulator.builder(8080),
        )
    ) as autd:
        await runner.run(autd)


if __name__ == "__main__":
    asyncio.run(main())
