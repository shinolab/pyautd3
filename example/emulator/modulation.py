from datetime import timedelta

import numpy as np
from matplotlib import pyplot as plt

from pyautd3 import AUTD3, Controller, EmitIntensity, Focus, Hz, Silencer, Sine, Uniform
from pyautd3.emulator import Emulator, Range, Recorder, RecordOption

if __name__ == "__main__":
    with Emulator([AUTD3([0.0, 0.0, 0.0])]) as emulator:
        # pulse width under 200Hz sine modulation with silencer
        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Silencer())
            autd.send((Sine(200.0 * Hz), Uniform(EmitIntensity(0xFF))))
            autd.tick(timedelta(milliseconds=10))
            return autd

        record = emulator.record(f)

        df = record.drive()
        t = df["time[ns]"]
        pulse_width = df["pulsewidth_0_0"]
        plt.plot(t / 1000_000, pulse_width)
        plt.xlim(5, 10)
        plt.ylim(0, 128)
        plt.xlabel("time [ms]")
        plt.ylabel("pulse width")
        plt.title("pulse width under 200Hz sine modulation with silencer")
        plt.show()

        # pulse width under 200Hz sine modulation without silencer
        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Silencer.disable())
            autd.send((Sine(200.0 * Hz), Uniform(EmitIntensity(0xFF))))
            autd.tick(timedelta(milliseconds=10))
            return autd

        record = emulator.record(f)

        df = record.drive()
        t = df["time[ns]"]
        pulse_width = df["pulsewidth_0_0"]
        plt.plot(t / 1000_000, pulse_width)
        plt.xlim(5, 10)
        plt.ylim(0, 128)
        plt.xlabel("time [ms]")
        plt.ylabel("pulse width")
        plt.title("pulse width under 200Hz sine modulation with silencer")
        plt.show()

        # plot sound pressure at focus under 200Hz sin modulation with silencer
        focus = emulator.geometry.center + np.array([0.0, 0.0, 150.0])

        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Silencer())
            autd.send((Sine(200.0 * Hz), Focus(focus)))
            autd.tick(timedelta(milliseconds=20))
            return autd

        record = emulator.record(f)

        print("Calculating sound pressure at focus under 200Hz sin modulation with silencer...")
        sound_field = record.sound_field(
            Range(
                x_start=focus[0],
                x_end=focus[0],
                y_start=focus[1],
                y_end=focus[1],
                z_start=focus[2],
                z_end=focus[2],
                resolution=1.0,
            ),
            RecordOption(
                time_step_ns=1000,
                print_progress=True,
            ),
        )

        df = sound_field.next(timedelta(milliseconds=20))
        time = np.array([float(t.replace("p[Pa]@", "").replace("[ns]", "")) for t in df.columns[3:]])
        p = df.row(0)[3:]
        plt.plot(time / 1000_000, p)
        plt.xlim(0, 20)
        plt.xlabel("time [ms]")
        plt.ylabel("p[Pa]")
        plt.title("sound pressure at focus under 200Hz sin modulation with silencer")
        plt.show()
