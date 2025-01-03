import numpy as np
from matplotlib import pyplot as plt

from pyautd3 import AUTD3, Controller, EmitIntensity, Focus, Hz, Silencer, Sine, Uniform
from pyautd3.emulator import InstantRecordOption, RangeXYZ, Recorder
from pyautd3.utils import Duration

if __name__ == "__main__":
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).into_emulator() as emulator:
        # pulse width under 200Hz sine modulation with silencer
        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Silencer())
            autd.send((Sine(200.0 * Hz), Uniform(EmitIntensity(0xFF))))
            autd.tick(Duration.from_millis(10))
            return autd

        record = emulator.record(f)

        df = record.pulse_width()
        t = [float(c.replace("pulse_width@", "").replace("[ns]", "")) / 1_000_000 for c in df.columns]
        pulse_width = df.row(0)
        plt.plot(t, pulse_width)
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
            autd.tick(Duration.from_millis(10))
            return autd

        record = emulator.record(f)

        df = record.pulse_width()
        t = [float(c.replace("pulse_width@", "").replace("[ns]", "")) / 1_000_000 for c in df.columns]
        pulse_width = df.row(0)
        plt.plot(t, pulse_width)
        plt.xlim(5, 10)
        plt.ylim(0, 128)
        plt.xlabel("time [ms]")
        plt.ylabel("pulse width")
        plt.title("pulse width under 200Hz sine modulation with silencer")
        plt.show()

        # plot sound pressure at focus under 200Hz sin modulation with silencer
        focus = emulator.center + np.array([0.0, 0.0, 150.0])

        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Silencer())
            autd.send((Sine(200.0 * Hz), Focus(focus)))
            autd.tick(Duration.from_millis(20))
            return autd

        record = emulator.record(f)

        print("Calculating sound pressure at focus under 200Hz sin modulation with silencer...")
        sound_field = record.sound_field(
            RangeXYZ(
                x_start=focus[0],
                x_end=focus[0],
                y_start=focus[1],
                y_end=focus[1],
                z_start=focus[2],
                z_end=focus[2],
                resolution=1.0,
            ),
            InstantRecordOption(
                time_step=Duration.from_micros(1),
                print_progress=True,
            ),
        )

        df = sound_field.next(Duration.from_millis(20))
        time = np.array([float(t.replace("p[Pa]@", "").replace("[ns]", "")) for t in df.columns])
        p = df.row(0)
        plt.plot(time / 1000_000, p)
        plt.xlim(0, 20)
        plt.xlabel("time [ms]")
        plt.ylabel("p[Pa]")
        plt.title("sound pressure at focus under 200Hz sin modulation with silencer")
        plt.show()
