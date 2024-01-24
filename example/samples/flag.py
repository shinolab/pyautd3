"""
File: flag.py
Project: samples
Created Date: 14/09/2023
Author: Shun Suzuki
-----
Last Modified: 23/01/2024
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2023 Shun Suzuki. All rights reserved.

"""


import threading

from pyautd3 import ConfigureForceFan, ConfigureReadsFPGAState, Controller


async def flag(autd: Controller) -> None:
    print("press any key to run fan...")
    _ = input()

    await autd.send_async(ConfigureReadsFPGAState(lambda _: True), ConfigureForceFan(lambda _: True))

    fin = False

    def f() -> None:
        nonlocal fin
        print("press any key stop checking FPGA status...")
        _ = input()
        fin = True

    th = threading.Thread(target=f)
    th.start()

    prompts = ["-", "/", "|", "\\"]
    prompts_idx = 0
    while not fin:
        states = await autd.fpga_state_async()
        print(f"{prompts[(prompts_idx // 1000) % len(prompts)]} FPGA Status...")
        print("\n".join([f"\x1b[0K[{i}]: thermo = {"-" if state is None else state.is_thermal_assert()}" for i, state in enumerate(states)]))
        print(f"\x1b[{len(states) + 1}A", end="")
        prompts_idx += 1
    print("\x1b[1F\x1b[0J")

    th.join()
    await autd.send_async(ConfigureReadsFPGAState(lambda _: False), ConfigureForceFan(lambda _: False))
