import ctypes
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from pyautd3.native_methods.autd3capi_driver import DynSincInterpolator, DynWindow


class Resampler(metaclass=ABCMeta):
    @abstractmethod
    def _dyn_resampler(self: "Resampler") -> DynSincInterpolator:
        pass


class BlackMan:
    _window_size: int

    def __init__(self: "BlackMan", window_size: int) -> None:
        self._window_size = window_size

    def _window(self: "BlackMan") -> ctypes.c_uint32:
        return ctypes.c_uint32(int(DynWindow.Blackman))


class Rectangular:
    _window_size: int

    def __init__(self: "Rectangular", window_size: int) -> None:
        self._window_size = window_size

    def _window(self: "Rectangular") -> ctypes.c_uint32:
        return ctypes.c_uint32(int(DynWindow.Rectangular))


T = TypeVar("T", BlackMan, Rectangular)


class SincInterpolation(
    Resampler,
    Generic[T],
):
    _window: T

    def __init__(self: "SincInterpolation", window: T | None = None) -> None:
        self._window = window if window is not None else BlackMan(32)

    def _dyn_resampler(self: "SincInterpolation") -> DynSincInterpolator:
        return DynSincInterpolator(self._window._window(), ctypes.c_uint32(self._window._window_size))
