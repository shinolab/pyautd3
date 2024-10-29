import ctypes
from abc import ABCMeta, abstractmethod
from typing import Self

import numpy as np

from pyautd3.driver.defined.angle import Angle
from pyautd3.driver.defined.freq import Freq
from pyautd3.native_methods.autd3_driver import SamplingConfig
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import LoopBehavior, ModulationPtr
from pyautd3.native_methods.utils import _validate_ptr


class ISamplingMode(metaclass=ABCMeta):
    @abstractmethod
    def sine_ptr(
        self: Self,
        config: SamplingConfig,
        intensity: int,
        offset: int,
        phase: Angle,
        clamp: bool,  # noqa: FBT001
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        pass

    @abstractmethod
    def sine_freq(self: Self) -> int | float:
        pass

    @abstractmethod
    def fourier_ptr(
        self: Self,
        components: list,
        size: int,
        clamp: bool,  # noqa: FBT001
        scale_factor: float,
        offset: int,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        pass

    @abstractmethod
    def square_ptr(
        self: Self,
        config: SamplingConfig,
        low: int,
        high: int,
        duty: float,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        pass

    @abstractmethod
    def square_freq(self: Self) -> int | float:
        pass


class SamplingModeExact(ISamplingMode):
    _freq: Freq[int]

    def __init__(self: Self, freq: Freq[int]) -> None:
        self._freq = freq

    def sine_ptr(
        self: Self,
        config: SamplingConfig,
        intensity: int,
        offset: int,
        phase: Angle,
        clamp: bool,  # noqa: FBT001
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_sine_exact(
                self._freq.hz,
                config,
                intensity,
                offset,
                phase.radian,
                clamp,
                loop_behavior,
            ),
        )

    def sine_freq(self: Self) -> int | float:
        return int(Base().modulation_sine_exact_freq(self._freq.hz))

    def fourier_ptr(
        self: Self,
        components: list,
        size: int,
        clamp: bool,  # noqa: FBT001
        scale_factor: float,
        offset: int,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        sine_freq = np.fromiter((m._mode._freq.hz for m in components), dtype=np.uint32)
        sine_config = np.fromiter((np.void(m._config._inner) for m in components), dtype=SamplingConfig)
        sine_intensity = np.fromiter((m._param_intensity_u8 for m in components), dtype=np.uint8)
        sine_offset = np.fromiter((m._param_offset_u8 for m in components), dtype=np.uint8)
        sine_phase = np.fromiter((m._param_phase.radian for m in components), dtype=np.float32)
        sine_clamp = np.fromiter((m._param_clamp for m in components), dtype=np.bool_)
        return _validate_ptr(
            Base().modulation_fourier_exact(
                sine_freq.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32)),  # type: ignore[arg-type]
                sine_config.ctypes.data_as(ctypes.POINTER(SamplingConfig)),  # type: ignore[arg-type]
                sine_intensity.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
                sine_offset.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
                sine_phase.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
                sine_clamp.ctypes.data_as(ctypes.POINTER(ctypes.c_bool)),  # type: ignore[arg-type]
                size,
                clamp,
                scale_factor,
                offset,
                loop_behavior,
            ),
        )

    def square_ptr(
        self: Self,
        config: SamplingConfig,
        low: int,
        high: int,
        duty: float,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_square_exact(
                self._freq.hz,
                config,
                low,
                high,
                duty,
                loop_behavior,
            ),
        )

    def square_freq(self: Self) -> int | float:
        return int(Base().modulation_square_exact_freq(self._freq.hz))


class SamplingModeExactFloat(ISamplingMode):
    _freq: Freq[float]

    def __init__(self: Self, freq: Freq[float]) -> None:
        self._freq = freq

    def sine_ptr(
        self: Self,
        config: SamplingConfig,
        intensity: int,
        offset: int,
        phase: Angle,
        clamp: bool,  # noqa: FBT001
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_sine_exact_float(
                self._freq.hz,
                config,
                intensity,
                offset,
                phase.radian,
                clamp,
                loop_behavior,
            ),
        )

    def sine_freq(self: Self) -> float:
        return float(Base().modulation_sine_exact_float_freq(self._freq.hz))

    def fourier_ptr(
        self: Self,
        components: list,
        size: int,
        clamp: bool,  # noqa: FBT001
        scale_factor: float,
        offset: int,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        sine_freq = np.fromiter((m._mode._freq.hz for m in components), dtype=np.float32)
        sine_config = np.fromiter((np.void(m._config._inner) for m in components), dtype=SamplingConfig)
        sine_intensity = np.fromiter((m._param_intensity_u8 for m in components), dtype=np.uint8)
        sine_offset = np.fromiter((m._param_offset_u8 for m in components), dtype=np.uint8)
        sine_phase = np.fromiter((m._param_phase.radian for m in components), dtype=np.float32)
        sine_clamp = np.fromiter((m._param_clamp for m in components), dtype=np.bool_)
        return _validate_ptr(
            Base().modulation_fourier_exact_float(
                sine_freq.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
                sine_config.ctypes.data_as(ctypes.POINTER(SamplingConfig)),  # type: ignore[arg-type]
                sine_intensity.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
                sine_offset.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
                sine_phase.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
                sine_clamp.ctypes.data_as(ctypes.POINTER(ctypes.c_bool)),  # type: ignore[arg-type]
                size,
                clamp,
                scale_factor,
                offset,
                loop_behavior,
            ),
        )

    def square_ptr(
        self: Self,
        config: SamplingConfig,
        low: int,
        high: int,
        duty: float,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_square_exact_float(
                self._freq.hz,
                config,
                low,
                high,
                duty,
                loop_behavior,
            ),
        )

    def square_freq(self: Self) -> float:
        return int(Base().modulation_square_exact_float_freq(self._freq.hz))


class SamplingModeNearest(ISamplingMode):
    _freq: Freq[float]

    def __init__(self: Self, freq: Freq[float]) -> None:
        self._freq = freq

    def sine_ptr(
        self: Self,
        config: SamplingConfig,
        intensity: int,
        offset: int,
        phase: Angle,
        clamp: bool,  # noqa: FBT001
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_sine_nearest(
                self._freq.hz,
                config,
                intensity,
                offset,
                phase.radian,
                clamp,
                loop_behavior,
            ),
        )

    def sine_freq(self: Self) -> int | float:
        return float(Base().modulation_sine_nearest_freq(self._freq.hz))

    def fourier_ptr(
        self: Self,
        components: list,
        size: int,
        clamp: bool,  # noqa: FBT001
        scale_factor: float,
        offset: int,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        sine_freq = np.fromiter((m._mode._freq.hz for m in components), dtype=np.float32)
        sine_config = np.fromiter((np.void(m._config._inner) for m in components), dtype=SamplingConfig)
        sine_intensity = np.fromiter((m._param_intensity_u8 for m in components), dtype=np.uint8)
        sine_offset = np.fromiter((m._param_offset_u8 for m in components), dtype=np.uint8)
        sine_phase = np.fromiter((m._param_phase.radian for m in components), dtype=np.float32)
        sine_clamp = np.fromiter((m._param_clamp for m in components), dtype=np.bool_)
        return _validate_ptr(
            Base().modulation_fourier_nearest(
                sine_freq.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
                sine_config.ctypes.data_as(ctypes.POINTER(SamplingConfig)),  # type: ignore[arg-type]
                sine_intensity.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
                sine_offset.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)),  # type: ignore[arg-type]
                sine_phase.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),  # type: ignore[arg-type]
                sine_clamp.ctypes.data_as(ctypes.POINTER(ctypes.c_bool)),  # type: ignore[arg-type]
                size,
                clamp,
                scale_factor,
                offset,
                loop_behavior,
            ),
        )

    def square_ptr(
        self: Self,
        config: SamplingConfig,
        low: int,
        high: int,
        duty: float,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_square_nearest(
                self._freq.hz,
                config,
                low,
                high,
                duty,
                loop_behavior,
            ),
        )

    def square_freq(self: Self) -> int | float:
        return int(Base().modulation_square_nearest_freq(self._freq.hz))
