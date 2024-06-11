import threading

from pyautd3 import Controller, ForceFan, ReadsFPGAState


def flag(autd: Controller) -> None:
    print("press any key to run fan...")
    _ = input()

    autd.send((ReadsFPGAState(lambda _: True), ForceFan(lambda _: True)))

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
        states = autd.fpga_state()
        print(f"{prompts[(prompts_idx // 1000) % len(prompts)]} FPGA Status...")
        print("\n".join([f"\x1b[0K[{i}]: thermo = {'-' if state is None else state.is_thermal_assert}" for i, state in enumerate(states)]))
        print(f"\x1b[{len(states) + 1}A", end="")
        prompts_idx += 1
    print("\x1b[1F\x1b[0J")

    th.join()
    autd.send((ReadsFPGAState(lambda _: False), ForceFan(lambda _: False)))
