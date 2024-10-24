from abc import ABCMeta, abstractmethod
from typing import Generic, Self, TypeVar

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_segment import DatagramS, IntoDatagramWithSegment
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.firmware.fpga import LoopBehavior
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, ModulationPtr, Segment, TransitionModeWrap
from pyautd3.native_methods.autd3capi_driver import LoopBehavior as _LoopBehavior

__all__ = []  # type: ignore[var-annotated]

M = TypeVar("M", bound="ModulationBase")


class ModulationBase(
    IntoDatagramWithSegment[M],
    DatagramS[ModulationPtr],
    Generic[M],
    IntoDatagramWithTimeout[M],
    IntoDatagramWithParallelThreshold[M],
    Datagram,
    metaclass=ABCMeta,
):
    _loop_behavior: _LoopBehavior

    def __init__(self: Self) -> None:
        super().__init__()
        self._loop_behavior = LoopBehavior.Infinite

    def _raw_ptr(self: Self, _: Geometry) -> ModulationPtr:
        return self._modulation_ptr()

    def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
        return Base().modulation_into_datagram(self._modulation_ptr())

    def _into_segment(
        self: Self,
        ptr: ModulationPtr,
        segment: Segment,
        transition_mode: TransitionModeWrap | None,
    ) -> DatagramPtr:
        return Base().modulation_into_datagram_with_segment(
            ptr,
            segment,
            transition_mode if transition_mode is not None else TransitionMode.NONE,
        )

    @abstractmethod
    def _modulation_ptr(self: Self) -> ModulationPtr:
        pass

    def with_loop_behavior(self: M, loop_behavior: _LoopBehavior) -> M:
        self._loop_behavior = loop_behavior
        return self

    @property
    def loop_behavior(self: Self) -> _LoopBehavior:
        return self._loop_behavior

    @property
    def sampling_config(self: Self) -> SamplingConfig:
        return SamplingConfig(Base().modulation_sampling_config(self._modulation_ptr()))

    def _sampling_config_intensity(self: Self) -> SamplingConfig:
        return self.sampling_config

    def _sampling_config_phase(self: Self) -> SamplingConfig:
        return SamplingConfig(0xFFFF)
