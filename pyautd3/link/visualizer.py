import ctypes
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable

import numpy as np

from pyautd3.autd_error import InvalidPlotConfigError
from pyautd3.driver.firmware.fpga.emit_intensity import EmitIntensity
from pyautd3.driver.firmware.fpga.phase import Phase
from pyautd3.driver.link import Link, LinkBuilder
from pyautd3.native_methods.autd3capi import ControllerPtr, RuntimePtr
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import LinkPtr, Segment
from pyautd3.native_methods.autd3capi_link_visualizer import (
    Backend,
    CMap,
    ConfigPtr,
    Directivity,
    LinkBuilderPtr,
    PlotConfigPtr,
    PlotRangePtr,
    PyPlotConfigPtr,
)
from pyautd3.native_methods.autd3capi_link_visualizer import (
    NativeMethods as LinkVisualizer,
)
from pyautd3.native_methods.structs import Vector3
from pyautd3.native_methods.utils import _validate_int, _validate_ptr

__all__ = [
    "PlottersBackend",
    "PythonBackend",
    "NullBackend",
    "Sphere",
    "T4010A1",
    "PlotRange",
    "PlotConfig",
    "PyPlotConfig",
    "NullPlotConfig",
    "Visualizer",
]  # type: ignore[var-annotated]


class IPlotBackend(metaclass=ABCMeta):
    _backend: Backend

    def __init__(self: "IPlotBackend", backend: Backend) -> None:
        self._backend = backend


class PlottersBackend(IPlotBackend):
    def __init__(self: "PlottersBackend") -> None:
        super().__init__(Backend.Plotters)


class PythonBackend(IPlotBackend):
    def __init__(self: "PythonBackend") -> None:
        super().__init__(Backend.Python)


class NullBackend(IPlotBackend):
    def __init__(self: "NullBackend") -> None:
        super().__init__(Backend.Null)


class IDirectivity(metaclass=ABCMeta):
    _directivity: Directivity

    def __init__(self: "IDirectivity", directivity: Directivity) -> None:
        self._directivity = directivity


class Sphere(IDirectivity):
    def __init__(self: "Sphere") -> None:
        super().__init__(Directivity.Sphere)


class T4010A1(IDirectivity):
    def __init__(self: "T4010A1") -> None:
        super().__init__(Directivity.T4010A1)


class PlotRange:
    x_start: float
    x_end: float
    y_start: float
    y_end: float
    z_start: float
    z_end: float
    resolution: float

    def __init__(
        self: "PlotRange",
        *,
        x_start: float = -0,
        x_end: float = 0,
        y_start: float = -0,
        y_end: float = 0,
        z_start: float = -0,
        z_end: float = 0,
        resolution: float = 1,
    ) -> None:
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.z_start = z_start
        self.z_end = z_end
        self.resolution = resolution

    def _ptr(self: "PlotRange") -> PlotRangePtr:
        return LinkVisualizer().link_visualizer_plot_range(
            self.x_start,
            self.x_end,
            self.y_start,
            self.y_end,
            self.z_start,
            self.z_end,
            self.resolution,
        )

    def observe_points(self: "PlotRange") -> list[np.ndarray]:
        plot_range = self._ptr()
        points_len = int(LinkVisualizer().link_visualizer_plot_range_observe_points_len(plot_range))
        buf = np.zeros(3 * points_len).astype(ctypes.c_float)
        LinkVisualizer().link_visualizer_plot_range_observe_points(plot_range, np.ctypeslib.as_ctypes(buf))
        return [np.array([buf[3 * i], buf[3 * i + 1], buf[3 * i + 2]]) for i in range(points_len)]


class IPlotConfig(metaclass=ABCMeta):
    @abstractmethod
    def _config_ptr(self: "IPlotConfig") -> ConfigPtr:
        pass

    @abstractmethod
    def _backend(self: "IPlotConfig") -> Backend:
        pass


class PlotConfig(IPlotConfig):
    figsize: tuple[int, int]
    cbar_size: float
    font_size: int
    label_area_size: int
    margin: int
    ticks_step: float
    cmap: CMap
    fname: str

    def __init__(
        self: "PlotConfig",
        *,
        figsize: tuple[int, int] | None = None,
        cbar_size: float | None = None,
        font_size: int | None = None,
        label_area_size: int | None = None,
        margin: int | None = None,
        ticks_step: float | None = None,
        cmap: CMap | None = None,
        fname: str,
    ) -> None:
        self.figsize = figsize if figsize is not None else (960, 640)
        self.cbar_size = cbar_size if cbar_size is not None else 0.15
        self.font_size = font_size if font_size is not None else 24
        self.label_area_size = label_area_size if label_area_size is not None else 80
        self.margin = margin if margin is not None else 10
        self.ticks_step = ticks_step if ticks_step is not None else 10
        self.cmap = cmap if cmap is not None else CMap.Jet
        self.fname = fname

    def _raw_ptr(self: "PlotConfig") -> PlotConfigPtr:
        return _validate_ptr(
            LinkVisualizer().link_visualizer_plot_config(
                self.figsize[0],
                self.figsize[1],
                self.cbar_size,
                self.font_size,
                self.label_area_size,
                self.margin,
                self.ticks_step,
                self.cmap,
                self.fname.encode("utf-8"),
            ),
        )

    def _config_ptr(self: "PlotConfig") -> ConfigPtr:
        return ConfigPtr(self._raw_ptr()._0)

    def _backend(self: "PlotConfig") -> Backend:
        return Backend.Plotters


class PyPlotConfig(IPlotConfig):
    figsize: tuple[int, int]
    dpi: int
    cbar_position: str
    cbar_size: str
    cbar_pad: str
    fontsize: int
    ticks_step: float
    cmap: str
    show: bool
    fname: str

    def __init__(
        self: "PyPlotConfig",
        *,
        figsize: tuple[int, int] | None = None,
        dpi: int | None = None,
        cbar_position: str | None = None,
        cbar_size: str | None = None,
        cbar_pad: str | None = None,
        fontsize: int | None = None,
        ticks_step: float | None = None,
        cmap: str | None = None,
        show: bool | None = None,
        fname: str,
    ) -> None:
        self.figsize = figsize if figsize is not None else (8, 6)
        self.dpi = dpi if dpi is not None else 72
        self.cbar_position = cbar_position if cbar_position is not None else "right"
        self.cbar_size = cbar_size if cbar_size is not None else "5%"
        self.cbar_pad = cbar_pad if cbar_pad is not None else "3%"
        self.fontsize = fontsize if fontsize is not None else 12
        self.ticks_step = ticks_step if ticks_step is not None else 10
        self.cmap = cmap if cmap is not None else "jet"
        self.show = show if show is not None else False
        self.fname = fname

    def _raw_ptr(self: "PyPlotConfig") -> PyPlotConfigPtr:
        return _validate_ptr(
            LinkVisualizer().link_visualizer_py_plot_config(
                self.figsize[0],
                self.figsize[1],
                self.dpi,
                self.cbar_position.encode("utf-8"),
                self.cbar_size.encode("utf-8"),
                self.cbar_pad.encode("utf-8"),
                self.fontsize,
                self.ticks_step,
                self.cmap.encode("utf-8"),
                self.show,
                self.fname.encode("utf-8"),
            ),
        )

    def _config_ptr(self: "PyPlotConfig") -> ConfigPtr:
        return ConfigPtr(self._raw_ptr()._0)

    def _backend(self: "PyPlotConfig") -> Backend:
        return Backend.Python


class NullPlotConfig(IPlotConfig):
    def _config_ptr(self: "NullPlotConfig") -> ConfigPtr:
        return ConfigPtr(LinkVisualizer().link_visualizer_null_plot_config()._0)

    def _backend(self: "NullPlotConfig") -> Backend:
        return Backend.Null


class Visualizer(Link):
    _ptr: LinkPtr
    _backend: Backend
    _directivity: Directivity

    class _Builder(LinkBuilder["Visualizer"]):
        _backend: Backend
        _directivity: Directivity
        _gpu_idx: int | None

        def __init__(self: "Visualizer._Builder", backend: Backend | None = None, directivity: Directivity | None = None) -> None:
            self._backend = backend if backend is not None else Backend.Plotters
            self._directivity = directivity if directivity is not None else Directivity.Sphere
            self._gpu_idx = None

        def _link_builder_ptr(self: "Visualizer._Builder") -> LinkBuilderPtr:
            match (self._backend, self._directivity):
                case (Backend.Plotters, Directivity.Sphere):
                    return LinkVisualizer().link_visualizer_sphere_plotters(
                        self._gpu_idx is not None,
                        self._gpu_idx if self._gpu_idx is not None else 0,
                    )
                case (Backend.Plotters, Directivity.T4010A1):
                    return LinkVisualizer().link_visualizer_t_4010_a_1_plotters(
                        self._gpu_idx is not None,
                        self._gpu_idx if self._gpu_idx is not None else 0,
                    )
                case (Backend.Python, Directivity.Sphere):
                    return LinkVisualizer().link_visualizer_sphere_python(
                        self._gpu_idx is not None,
                        self._gpu_idx if self._gpu_idx is not None else 0,
                    )
                case (Backend.Python, Directivity.T4010A1):
                    return LinkVisualizer().link_visualizer_t_4010_a_1_python(
                        self._gpu_idx is not None,
                        self._gpu_idx if self._gpu_idx is not None else 0,
                    )
                case (Backend.Null, Directivity.Sphere):
                    return LinkVisualizer().link_visualizer_sphere_null(
                        self._gpu_idx is not None,
                        self._gpu_idx if self._gpu_idx is not None else 0,
                    )
                case (Backend.Null, Directivity.T4010A1):
                    return LinkVisualizer().link_visualizer_t_4010_a_1_null(
                        self._gpu_idx is not None,
                        self._gpu_idx if self._gpu_idx is not None else 0,
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError

        def _resolve_link(self: "Visualizer._Builder", runtime: RuntimePtr, ptr: ControllerPtr) -> "Visualizer":
            return Visualizer(runtime, Base().link_get(ptr), self._backend, self._directivity)

        def with_gpu(self: "Visualizer._Builder", gpu_idx: int) -> "Visualizer._Builder":  # pragma: no cover
            self._gpu_idx = gpu_idx
            return self

        def with_backend(self: "Visualizer._Builder", backend: IPlotBackend) -> "Visualizer._Builder":
            self._backend = backend._backend
            return self

        def with_directivity(self: "Visualizer._Builder", directivity: IDirectivity) -> "Visualizer._Builder":
            self._directivity = directivity._directivity
            return self

    def __init__(self: "Visualizer", runtime: RuntimePtr, ptr: LinkPtr, backend: Backend, directivity: Directivity) -> None:
        super().__init__(runtime, ptr)
        self._backend = backend
        self._directivity = directivity

    @staticmethod
    def builder() -> _Builder:
        return Visualizer._Builder()

    @staticmethod
    def plotters() -> _Builder:
        return Visualizer._Builder(Backend.Plotters)

    @staticmethod
    def python() -> _Builder:
        return Visualizer._Builder(Backend.Python)

    @staticmethod
    def null() -> _Builder:
        return Visualizer._Builder(Backend.Null)

    def phases(self: "Visualizer", segment: Segment, idx: int) -> np.ndarray:
        size = LinkVisualizer().link_visualizer_phases_of(self._ptr, self._backend, self._directivity, segment, idx, None)
        phases = np.zeros(int(size)).astype(ctypes.c_uint8)
        LinkVisualizer().link_visualizer_phases_of(self._ptr, self._backend, self._directivity, segment, idx, np.ctypeslib.as_ctypes(phases))
        return np.fromiter((Phase(int(x)) for x in phases), dtype=Phase)

    def intensities(self: "Visualizer", segment: Segment, idx: int) -> np.ndarray:
        size = LinkVisualizer().link_visualizer_intensities(self._ptr, self._backend, self._directivity, segment, idx, None)
        intensities = np.zeros(int(size)).astype(ctypes.c_uint8)
        LinkVisualizer().link_visualizer_intensities(self._ptr, self._backend, self._directivity, segment, idx, np.ctypeslib.as_ctypes(intensities))
        return np.fromiter((EmitIntensity(int(x)) for x in intensities), dtype=EmitIntensity)

    def modulation(self: "Visualizer", segment: Segment) -> np.ndarray:
        size = LinkVisualizer().link_visualizer_modulation(self._ptr, self._backend, self._directivity, segment, None)
        modulation = np.zeros(int(size)).astype(ctypes.c_uint8)
        LinkVisualizer().link_visualizer_modulation(self._ptr, self._backend, self._directivity, segment, np.ctypeslib.as_ctypes(modulation))
        return modulation

    def calc_field(self: "Visualizer", points_iter: Iterable[np.ndarray], segment: Segment, idx: int) -> np.ndarray:
        points = np.fromiter((np.void(Vector3(d)) for d in points_iter), dtype=Vector3)  # type: ignore[type-var,call-overload]
        points_len = len(points)
        buf = np.zeros(points_len * 2).astype(ctypes.c_float)
        _validate_int(
            LinkVisualizer().link_visualizer_calc_field(
                self._ptr,
                self._backend,
                self._directivity,
                points.ctypes.data_as(ctypes.POINTER(Vector3)),  # type: ignore[arg-type]
                points_len,
                segment,
                idx,
                np.ctypeslib.as_ctypes(buf),
            ),
        )
        return np.fromiter([buf[2 * i] + buf[2 * i + 1] * 1j for i in range(points_len)], dtype=np.complex128, count=points_len)

    def plot_field(self: "Visualizer", config: IPlotConfig, plot_range: PlotRange, segment: Segment, idx: int) -> None:
        if self._backend != config._backend():
            raise InvalidPlotConfigError
        _validate_int(
            LinkVisualizer().link_visualizer_plot_field(
                self._ptr,
                self._backend,
                self._directivity,
                config._config_ptr(),
                plot_range._ptr(),
                segment,
                idx,
            ),
        )

    def plot_phase(self: "Visualizer", config: IPlotConfig, segment: Segment, idx: int) -> None:
        if self._backend != config._backend():
            raise InvalidPlotConfigError
        _validate_int(
            LinkVisualizer().link_visualizer_plot_phase(
                self._ptr,
                self._backend,
                self._directivity,
                config._config_ptr(),
                segment,
                idx,
            ),
        )

    def plot_modulation(self: "Visualizer", config: IPlotConfig, segment: Segment) -> None:
        if self._backend != config._backend():
            raise InvalidPlotConfigError
        _validate_int(LinkVisualizer().link_visualizer_plot_modulation(self._ptr, self._backend, self._directivity, config._config_ptr(), segment))
