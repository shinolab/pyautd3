from matplotlib import pyplot as plt

from pyautd3 import AUTD3, Controller, EmitIntensity, Phase, Silencer, Static, Uniform
from pyautd3.emulator import Recorder
from pyautd3.utils import Duration

if __name__ == "__main__":
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).into_emulator() as emulator:
        # output voltage
        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Silencer.disable())
            autd.send((Static.with_intensity(0xFF), Uniform((Phase(0x40), EmitIntensity(0xFF)))))
            autd.tick(Duration.from_millis(1))
            return autd

        record = emulator.record(f)

        df = record.output_voltage()
        t = df["time[25us/256]"]
        pulse_width = df["voltage_0_0[V]"]
        plt.plot(t * 25 / 256 / 1000, pulse_width)
        plt.xlim(0, 1)
        plt.ylim(-15, 15)
        plt.xlabel("time [ms]")
        plt.ylabel("Voltage [V]")
        plt.title("output voltage")
        plt.show()

        df = record.output_ultrasound()
        t = df["time[25us/256]"]
        pulse_width = df["p_0_0[a.u.]"]
        plt.plot(t * 25 / 256 / 1000, pulse_width)
        plt.xlim(0, 1)
        plt.ylim(-1.1, 1.1)
        plt.xlabel("time [ms]")
        plt.ylabel("p [a.u.]")
        plt.title("output ultrasound")
        plt.show()
