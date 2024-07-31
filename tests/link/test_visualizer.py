import numpy as np
import pytest

from pyautd3 import AUTD3, Controller, EmitIntensity, Phase, Segment
from pyautd3.autd_error import InvalidPlotConfigError
from pyautd3.gain import Uniform
from pyautd3.link.visualizer import (
    T4010A1,
    CMap,
    IPlotConfig,
    NullBackend,
    NullPlotConfig,
    PlotConfig,
    PlotRange,
    PlottersBackend,
    PyPlotConfig,
    PythonBackend,
    Sphere,
    Visualizer,
)
from pyautd3.modulation import Static
from pyautd3.native_methods.autd3capi_link_visualizer import NativeMethods as Vis


def visualizer_test_with(autd: Controller[Visualizer], config: IPlotConfig):
    center = autd.geometry.center + np.array([0, 0, 150])

    g = Uniform((EmitIntensity(0x80), Phase(0x81)))
    m = Static().with_intensity(0x82)

    autd.send((m, g))

    autd.link.plot_phase(
        config,
        Segment.S0,
        0,
    )
    autd.link.plot_field(
        config,
        PlotRange(
            x_start=center[0] - 50,
            x_end=center[0] + 50,
            y_start=center[1],
            y_end=center[1],
            z_start=center[2],
            z_end=center[2],
            resolution=1,
        ),
        Segment.S0,
        0,
    )
    autd.link.plot_field(
        config,
        PlotRange(
            x_start=center[0] - 20,
            x_end=center[0] + 20,
            y_start=center[1] - 30,
            y_end=center[1] + 30,
            z_start=center[2],
            z_end=center[2],
            resolution=1,
        ),
        Segment.S0,
        0,
    )
    autd.link.plot_modulation(config, Segment.S0)

    intensities = autd.link.intensities(Segment.S0, 0)
    assert np.array_equal(intensities, np.array([EmitIntensity(0x80)] * autd.geometry.num_transducers))
    phases = autd.link.phases(Segment.S0, 0)
    assert np.array_equal(phases, np.array([Phase(0x81)] * autd.geometry.num_transducers))
    assert np.array_equal(autd.link.modulation(Segment.S0), np.array([0x82] * 2))

    points = [center]
    autd.link.calc_field(points, Segment.S0, 0)

    autd.close()


def test_plot_range():
    plot_range = PlotRange(
        x_start=-20,
        x_end=20,
        y_start=-30,
        y_end=30,
        z_start=0,
        z_end=0,
        resolution=1,
    )
    points = plot_range.observe_points()
    assert len(points) == 41 * 61
    assert np.array_equal(points[0], [-20, -30, 0])
    assert np.array_equal(points[1], [-19, -30, 0])
    assert np.array_equal(points[-1], [20, 30, 0])


def test_visualizer_plotters():
    with (
        Controller[Visualizer]
        .builder([AUTD3([0.0, 0.0, 0.0])])
        .open(
            Visualizer.builder().with_backend(PlottersBackend()).with_directivity(Sphere()),  # type: ignore[arg-type]
        ) as autd
    ):
        visualizer_test_with(
            autd,
            PlotConfig(fname="test.png"),
        )

    with (
        Controller[Visualizer]
        .builder([AUTD3([0.0, 0.0, 0.0])])
        .open(
            Visualizer.plotters().with_directivity(T4010A1()),  # type: ignore[arg-type]
        ) as autd
    ):
        visualizer_test_with(
            autd,
            PlotConfig(
                fname="test.png",
                figsize=(960, 640),
                cbar_size=0.15,
                font_size=24,
                label_area_size=80,
                margin=10,
                ticks_step=10.0,
                cmap=CMap.Jet,
            ),
        )


def test_visualizer_python():
    with (
        Controller[Visualizer]
        .builder([AUTD3([0.0, 0.0, 0.0])])
        .open(
            Visualizer.builder().with_backend(PythonBackend()).with_directivity(Sphere()),  # type: ignore[arg-type]
        ) as autd
    ):
        visualizer_test_with(
            autd,
            PyPlotConfig(fname="test.png"),
        )

    with (
        Controller[Visualizer]
        .builder([AUTD3([0.0, 0.0, 0.0])])
        .open(
            Visualizer.python().with_directivity(T4010A1()),  # type: ignore[arg-type]
        ) as autd
    ):
        visualizer_test_with(
            autd,
            PyPlotConfig(
                fname="test.png",
                figsize=(8, 6),
                dpi=72,
                cbar_position="right",
                cbar_size="5%",
                cbar_pad="3%",
                fontsize=12,
                ticks_step=10.0,
                cmap="jet",
                show=False,
            ),
        )


def test_visualizer_null():
    with (
        Controller[Visualizer]
        .builder([AUTD3([0.0, 0.0, 0.0])])
        .open(
            Visualizer.builder().with_backend(NullBackend()).with_directivity(Sphere()),  # type: ignore[arg-type]
        ) as autd
    ):
        visualizer_test_with(autd, NullPlotConfig())

    with (
        Controller[Visualizer]
        .builder([AUTD3([0.0, 0.0, 0.0])])
        .open(
            Visualizer.null().with_directivity(T4010A1()),  # type: ignore[arg-type]
        ) as autd
    ):
        visualizer_test_with(autd, NullPlotConfig())


@pytest.mark.gpu()
def test_visualizer_gpu():
    with (
        Controller[Visualizer]
        .builder([AUTD3([0.0, 0.0, 0.0])])
        .open(
            Visualizer.null().with_gpu(-1),  # type: ignore[arg-type]
        ) as autd
    ):
        visualizer_test_with(autd, NullPlotConfig())


def test_visualizer_invalid_config():
    autd: Controller[Visualizer]
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(
        Visualizer.builder().with_backend(PlottersBackend()).with_directivity(Sphere()),  # type: ignore[arg-type]
    ) as autd:
        center = autd.geometry.center + np.array([0, 0, 150])
        with pytest.raises(InvalidPlotConfigError):
            autd.link.plot_field(
                PyPlotConfig(fname="test.png"),
                PlotRange(
                    x_start=center[0] - 20,
                    x_end=center[0] + 20,
                    y_start=center[1] - 30,
                    y_end=center[1] + 30,
                    z_start=center[2],
                    z_end=center[2],
                    resolution=1,
                ),
                Segment.S0,
                0,
            )
        with pytest.raises(InvalidPlotConfigError):
            autd.link.plot_phase(
                PyPlotConfig(fname="test.png"),
                Segment.S0,
                0,
            )
        with pytest.raises(InvalidPlotConfigError):
            autd.link.plot_modulation(
                NullPlotConfig(),
                Segment.S0,
            )


def test_visualizer_config_default():
    m = PlotConfig(fname="")
    assert Vis().link_visualizer_plot_config_is_default(m._raw_ptr())


def test_visualizer_pyconfig_default():
    m = PyPlotConfig(fname="fig.png")
    assert Vis().link_visualizer_py_plot_config_is_default(m._raw_ptr())
