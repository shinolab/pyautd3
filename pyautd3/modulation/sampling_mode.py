import ctypes
from abc import ABCMeta, abstractmethod

import numpy as np

from pyautd3.driver.defined.angle import Angle
from pyautd3.driver.defined.freq import Freq
from pyautd3.driver.firmware.fpga import EmitIntensity
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import LoopBehavior, ModulationPtr, SamplingConfigWrap
from pyautd3.native_methods.utils import _validate_ptr


class ISamplingMode(metaclass=ABCMeta):
    @abstractmethod
    def sine_ptr(
        self: "ISamplingMode",
        config: SamplingConfigWrap,
        intensity: EmitIntensity,
        offset: EmitIntensity,
        phase: Angle,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
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
        config: SamplingConfigWrap,
        low: EmitIntensity,
        high: EmitIntensity,
        duty: float,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        pass


class SamplingModeExact(ISamplingMode):
    _freq: Freq[int]

    def __init__(self: "SamplingModeExact", freq: Freq[int]) -> None:
        self._freq = freq

    def sine_ptr(
        self: "SamplingModeExact",
        config: SamplingConfigWrap,
        intensity: EmitIntensity,
        offset: EmitIntensity,
        phase: Angle,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return Base().modulation_sine_exact(self._freq.hz, config, intensity.value, offset.value, phase.radian, loop_behavior)

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
        config: SamplingConfigWrap,
        low: EmitIntensity,
        high: EmitIntensity,
        duty: float,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return Base().modulation_square_exact(self._freq.hz, config, low.value, high.value, duty, loop_behavior)


class SamplingModeExactFloat(ISamplingMode):
    _freq: Freq[float]

    def __init__(self: "SamplingModeExactFloat", freq: Freq[float]) -> None:
        self._freq = freq

    def sine_ptr(
        self: "SamplingModeExactFloat",
        config: SamplingConfigWrap,
        intensity: EmitIntensity,
        offset: EmitIntensity,
        phase: Angle,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return Base().modulation_sine_exact_float(self._freq.hz, config, intensity.value, offset.value, phase.radian, loop_behavior)

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
        config: SamplingConfigWrap,
        low: EmitIntensity,
        high: EmitIntensity,
        duty: float,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return Base().modulation_square_exact_float(self._freq.hz, config, low.value, high.value, duty, loop_behavior)


class SamplingModeNearest(ISamplingMode):
    _freq: Freq[float]

    def __init__(self: "SamplingModeNearest", freq: Freq[float]) -> None:
        self._freq = freq

    def sine_ptr(
        self: "SamplingModeNearest",
        config: SamplingConfigWrap,
        intensity: EmitIntensity,
        offset: EmitIntensity,
        phase: Angle,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return Base().modulation_sine_nearest(self._freq.hz, config, intensity.value, offset.value, phase.radian, loop_behavior)

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
        config: SamplingConfigWrap,
        low: EmitIntensity,
        high: EmitIntensity,
        duty: float,
        loop_behavior: LoopBehavior,
    ) -> ModulationPtr:
        return Base().modulation_square_nearest(self._freq.hz, config, low.value, high.value, duty, loop_behavior)
