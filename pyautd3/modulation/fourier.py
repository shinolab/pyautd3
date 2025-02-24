import ctypes
from collections.abc import Iterable
from typing import Self

import numpy as np

from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.modulation.sine import Sine, SineMode
from pyautd3.native_methods.autd3capi import FourierOption as FourierOption_
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import SineOption as SineOption_
from pyautd3.native_methods.autd3capi_driver import ModulationPtr


class FourierOption:
    scale_factor: float | None
    clamp: bool
    offset: int

    def __init__(
        self: Self,
        *,
        scale_factor: float | None = None,
        clamp: bool = False,
        offset: int = 0,
    ) -> None:
        self.scale_factor = scale_factor
        self.clamp = clamp or False
        self.offset = offset or 0

    def _inner(self: Self) -> FourierOption_:
        return FourierOption_(
            self.scale_factor is not None,
            self.scale_factor or float("nan"),
            self.clamp,
            self.offset,
        )


class Fourier(Modulation):
    components: list[Sine]
    option: FourierOption

    def __init__(self: Self, components: Iterable[Sine], option: FourierOption) -> None:
        super().__init__()
        self.components = list(components)
        self.option = option

    def _modulation_ptr(self: Self) -> ModulationPtr:
        size = len(self.components)
        option = self.option._inner()

        sine_option = np.fromiter((np.void(m.option._inner()) for m in self.components), dtype=SineOption_)  # type: ignore[type-var,call-overload]
        match self.components[0]._mode:
            case SineMode.Exact:
                sine_freq = np.fromiter((m.freq.hz() for m in self.components), dtype=np.uint32)
                return Base().modulation_fourier_exact(
                    sine_freq.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)),  # type: ignore[arg-type]
                    sine_option.ctypes.data_as(ctypes.POINTER(SineOption_)),  # type: ignore[arg-type]
                    size,
                    option,
                )
            case SineMode.ExactFloat:
                sine_freq = np.fromiter((m.freq.hz() for m in self.components), dtype=np.float32)
                return Base().modulation_fourier_exact_float(
                    sine_freq.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
                    sine_option.ctypes.data_as(ctypes.POINTER(SineOption_)),  # type: ignore[arg-type]
                    size,
                    option,
                )
            case SineMode.Nearest:  # pragma: no cover
                sine_freq = np.fromiter((m.freq.hz() for m in self.components), dtype=np.float32)
                return Base().modulation_fourier_nearest(
                    sine_freq.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
                    sine_option.ctypes.data_as(ctypes.POINTER(SineOption_)),  # type: ignore[arg-type]
                    size,
                    option,
                )
