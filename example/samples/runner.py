from pyautd3 import Controller, Null, Silencer

from . import bessel, custom, flag, focus, group, holo, plane, stm, wav


def run(autd: Controller) -> None:
    samples = [
        (focus.simple, "Single focus test"),
        (bessel.bessel, "Bessel beam test"),
        (plane.plane, "Plane wave test"),
        (wav.wav, "Wav modulation test"),
        (stm.stm_focus, "FociSTM test"),
        (stm.stm_gain, "GainSTM test"),
        (holo.holo, "Multiple foci test"),
        (flag.flag, "Flag test"),
        (custom.custom, "Custom gain test"),
        (group.group_by_transducer, "Group (by Transducer) test"),
    ]

    if autd.num_devices >= 2:
        samples.append((group.group_by_device, "Group (by Device) test"))

    print("======== AUTD3 firmware information ========")
    print("\n".join([str(firm) for firm in autd.firmware_version()]))
    print("============================================")

    while True:
        print("\n".join([f"[{i}]: {name}" for i, (_, name) in enumerate(samples)]))
        print("[Other]: finish")

        input_str = input("choose number: ")
        idx = int(input_str) if input_str.isdigit() else len(samples)
        if idx >= len(samples):
            break

        (fn, _) = samples[idx]
        fn(autd)

        print("press enter to finish...")

        _ = input()

        print("finish.")
        autd.send((Null(), Silencer()))

    autd.close()
