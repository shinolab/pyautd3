import numpy as np
from matplotlib import animation, colorbar
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize

from pyautd3 import AUTD3, Controller, FociSTM, Focus, SamplingConfig, Silencer, Static, kHz
from pyautd3.emulator import RangeXYZ, Recorder, RmsRecordOption
from pyautd3.utils import Duration


def plot_focus() -> None:

    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).into_emulator() as emulator:
        focus = emulator.center + np.array([0.0, 0.0, 150.0])

        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Silencer.disable())
            autd.send((Static.with_intensity(0xFF), Focus(focus)))
            autd.tick(Duration.from_micros(25))
            return autd

        record = emulator.record(f)

        sound_field = record.sound_field(
            RangeXYZ(
                x_start=focus[0] - 20.0,
                x_end=focus[0] + 20.0,
                y_start=focus[1] - 20.0,
                y_end=focus[1] + 20.0,
                z_start=focus[2],
                z_end=focus[2],
                resolution=1.0,
            ),
            RmsRecordOption(
                print_progress=True,
                gpu=True,
            ),
        )
        print("Calculating sound field around focus...")

        df = sound_field.observe_points()
        x = np.unique(df["x[mm]"])
        y = np.unique(df["y[mm]"])

        df = sound_field.next(Duration.from_micros(25))

        rms = df.get_columns()[0].to_numpy().reshape([len(y), len(x)])
        aspect = (len(x), len(y), len(x))
        x, y = np.meshgrid(x, y)

        # plot RMS
        fig = plt.figure()
        spec = fig.add_gridspec(ncols=2, nrows=1, width_ratios=[10, 1])
        ax = fig.add_subplot(spec[0], projection="3d")
        cax = fig.add_subplot(spec[1])
        ax.plot_surface(  # type: ignore[attr-defined]
            x,
            y,
            rms,
            shade=False,
            cmap="jet",
            norm=Normalize(vmin=0.0, vmax=rms.max()),  # type: ignore[arg-type]
        )
        ax.set_box_aspect(aspect)  # type: ignore[arg-type]
        colorbar.ColorbarBase(cax, cmap="jet", norm=Normalize(vmin=0.0, vmax=rms.max()))  # type: ignore[arg-type]
        plt.show()


def plot_stm() -> None:
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).into_emulator() as emulator:
        focus = emulator.center + np.array([0.0, 0.0, 150.0])

        def f(autd: Controller[Recorder]) -> Controller[Recorder]:
            autd.send(Silencer())
            autd.send(
                (
                    Static.with_intensity(0xFF),
                    FociSTM(
                        SamplingConfig(1.0 * kHz),
                        (focus + 20.0 * np.array([np.cos(theta), np.sin(theta), 0]) for theta in (2.0 * np.pi * i / 4 for i in range(4))),
                    ),
                ),
            )
            autd.tick(Duration.from_millis(5))
            return autd

        record = emulator.record(f)

        sound_field = record.sound_field(
            RangeXYZ(
                x_start=focus[0] - 30.0,
                x_end=focus[0] + 30.0,
                y_start=focus[1] - 30.0,
                y_end=focus[1] + 30.0,
                z_start=focus[2],
                z_end=focus[2],
                resolution=1.0,
            ),
            RmsRecordOption(
                print_progress=True,
                gpu=True,
            ),
        )
        print("Calculating sound field around focus...")

        df = sound_field.observe_points()
        x = np.unique(df["x[mm]"])
        y = np.unique(df["y[mm]"])

        df = sound_field.next(Duration.from_millis(5))

        times = [float(c.replace("rms[Pa]@", "").replace("[ns]", "")) / 1000_000 for c in df.columns]
        rms = df.get_columns()

        times = times[70:]
        rms = rms[70:]

        fig = plt.figure()
        spec = fig.add_gridspec(ncols=2, nrows=1, width_ratios=[10, 1])
        ax = fig.add_subplot(spec[0], projection="3d")
        cax = fig.add_subplot(spec[1])
        colorbar.ColorbarBase(cax, cmap="jet", norm=Normalize(vmin=-0, vmax=5e3))

        rms_shape = [len(y), len(x)]
        aspect = (len(x), len(y), len(x))
        x, y = np.meshgrid(x, y)

        def anim(i: int):  # noqa: ANN202
            ax.cla()
            z = rms[i].to_numpy().reshape(rms_shape)
            plot = ax.plot_surface(x, y, z, shade=False, cmap="jet", norm=Normalize(vmin=0, vmax=5e3))  # type: ignore[attr-defined]
            ax.set_zlim(0, 5e3)  # type: ignore[attr-defined]
            ax.set_box_aspect(aspect)  # type: ignore[arg-type]
            ax.set_title(f"t={times[i]:.3f} [ms]")
            return plot

        _ = animation.FuncAnimation(fig, anim, frames=len(rms), interval=1, repeat=False, blit=False)
        plt.show()


if __name__ == "__main__":
    print("INFO: rms does not take into account propagation delay nor transducer response.")
    plot_focus()
    plot_stm()
