import ctypes
from abc import ABCMeta, abstractmethod

import numpy as np

from pyautd3.driver.defined.angle import Angle
from pyautd3.driver.defined.freq import Freq
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import LoopBehavior, ModulationPtr
from pyautd3.native_methods.structs import SamplingConfig
from pyautd3.native_methods.utils import _validate_ptr


class ISamplingMode(metaclass=ABCMeta):
    @abstractmethod
    def sine_ptr(
        self: "ISamplingMode",
        config: SamplingConfig,
        intensity: int,
        offset: int,
        phase: Angle,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        pass

    @abstractmethod
    def sine_freq(self: "ISamplingMode", ptr: ModulationPtr) -> int | float:
        pass

    @abstractmethod
    def fourier_ptr(self: "ISamplingMode", components: np.ndarray, size: int, loop_behavior: LoopBehavior) -> ModulationPtr:
        pass

    @abstractmethod
    def mixer_ptr(self: "ISamplingMode", components: np.ndarray, size: int, loop_behavior: LoopBehavior) -> ModulationPtr:
        pass

    @abstractmethod
    def square_ptr(
        self: "ISamplingMode",
        config: SamplingConfig,
        low: int,
        high: int,
        duty: float,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        pass

    @abstractmethod
    def square_freq(self: "ISamplingMode", ptr: ModulationPtr) -> int | float:
        pass


class SamplingModeExact(ISamplingMode):
    _freq: Freq[int]

    def __init__(self: "SamplingModeExact", freq: Freq[int]) -> None:
        self._freq = freq

    def sine_ptr(
        self: "SamplingModeExact",
        config: SamplingConfig,
        intensity: int,
        offset: int,
        phase: Angle,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_sine_exact(
                self._freq.hz,
                config,
                intensity,
                offset,
                phase.radian,
                loop_behavior,
            ),
        )

    def sine_freq(self: "SamplingModeExact", ptr: ModulationPtr) -> int | float:
        return int(Base().modulation_sine_exact_freq(ptr))

    def fourier_ptr(self: "SamplingModeExact", components: np.ndarray, size: int, loop_behavior: LoopBehavior) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_fourier_exact(
                components.ctypes.data_as(ctypes.POINTER(ModulationPtr)),  # type: ignore[arg-type]
                size,
                loop_behavior,
            ),
        )

    def mixer_ptr(self: "SamplingModeExact", components: np.ndarray, size: int, loop_behavior: LoopBehavior) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_mixer_exact(
                components.ctypes.data_as(ctypes.POINTER(ModulationPtr)),  # type: ignore[arg-type]
                size,
                loop_behavior,
            ),
        )

    def square_ptr(
        self: "SamplingModeExact",
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

    def square_freq(self: "SamplingModeExact", ptr: ModulationPtr) -> int | float:
        return int(Base().modulation_square_exact_freq(ptr))


class SamplingModeExactFloat(ISamplingMode):
    _freq: Freq[float]

    def __init__(self: "SamplingModeExactFloat", freq: Freq[float]) -> None:
        self._freq = freq

    def sine_ptr(
        self: "SamplingModeExactFloat",
        config: SamplingConfig,
        intensity: int,
        offset: int,
        phase: Angle,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_sine_exact_float(
                self._freq.hz,
                config,
                intensity,
                offset,
                phase.radian,
                loop_behavior,
            ),
        )

    def sine_freq(
        self: "SamplingModeExactFloat",
        ptr: ModulationPtr,
    ) -> int | float:
        return float(Base().modulation_sine_exact_float_freq(ptr))

    def fourier_ptr(self: "SamplingModeExactFloat", components: np.ndarray, size: int, loop_behavior: LoopBehavior) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_fourier_exact_float(
                components.ctypes.data_as(ctypes.POINTER(ModulationPtr)),  # type: ignore[arg-type]
                size,
                loop_behavior,
            ),
        )

    def mixer_ptr(self: "SamplingModeExactFloat", components: np.ndarray, size: int, loop_behavior: LoopBehavior) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_mixer_exact_float(
                components.ctypes.data_as(ctypes.POINTER(ModulationPtr)),  # type: ignore[arg-type]
                size,
                loop_behavior,
            ),
        )

    def square_ptr(
        self: "SamplingModeExactFloat",
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

    def square_freq(self: "SamplingModeExactFloat", ptr: ModulationPtr) -> int | float:
        return int(Base().modulation_square_exact_float_freq(ptr))


class SamplingModeNearest(ISamplingMode):
    _freq: Freq[float]

    def __init__(self: "SamplingModeNearest", freq: Freq[float]) -> None:
        self._freq = freq

    def sine_ptr(
        self: "SamplingModeNearest",
        config: SamplingConfig,
        intensity: int,
        offset: int,
        phase: Angle,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_sine_nearest(
                self._freq.hz,
                config,
                intensity,
                offset,
                phase.radian,
                loop_behavior,
            ),
        )

    def sine_freq(self: "SamplingModeNearest", ptr: ModulationPtr) -> int | float:
        return float(Base().modulation_sine_nearest_freq(ptr))

    def fourier_ptr(self: "SamplingModeNearest", components: np.ndarray, size: int, loop_behavior: LoopBehavior) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_fourier_nearest(
                components.ctypes.data_as(ctypes.POINTER(ModulationPtr)),  # type: ignore[arg-type]
                size,
                loop_behavior,
            ),
        )

    def mixer_ptr(self: "SamplingModeNearest", components: np.ndarray, size: int, loop_behavior: LoopBehavior) -> ModulationPtr:
        return _validate_ptr(
            Base().modulation_mixer_nearest(
                components.ctypes.data_as(ctypes.POINTER(ModulationPtr)),  # type: ignore[arg-type]
                size,
                loop_behavior,
            ),
        )

    def square_ptr(
        self: "SamplingModeNearest",
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

    def square_freq(self: "SamplingModeNearest", ptr: ModulationPtr) -> int | float:
        return int(Base().modulation_square_nearest_freq(ptr))
