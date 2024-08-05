from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_segment_transition import DatagramST, IntoDatagramWithSegmentTransition
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.firmware.fpga import LoopBehavior
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, ModulationPtr, Segment, TransitionModeWrap
from pyautd3.native_methods.autd3capi_driver import LoopBehavior as _LoopBehavior

__all__ = []  # type: ignore[var-annotated]

M = TypeVar("M", bound="ModulationBase")


class ModulationBase(
    IntoDatagramWithSegmentTransition[M],
    DatagramST[ModulationPtr],
    Generic[M],
    IntoDatagramWithTimeout[M],
    IntoDatagramWithParallelThreshold[M],
    Datagram,
    metaclass=ABCMeta,
):
    _loop_behavior: _LoopBehavior

    def __init__(self: "ModulationBase[M]") -> None:
        super().__init__()
        self._loop_behavior = LoopBehavior.Infinite

    def _raw_ptr(self: "ModulationBase[M]", _: Geometry) -> ModulationPtr:
        return self._modulation_ptr()

    def _datagram_ptr(self: "ModulationBase[M]", _: Geometry) -> DatagramPtr:
        return Base().modulation_into_datagram(self._modulation_ptr())

    def _into_segment_transition(
        self: "ModulationBase[M]",
        ptr: ModulationPtr,
        segment: Segment,
        transition_mode: TransitionModeWrap | None,
    ) -> DatagramPtr:
        if transition_mode is None:
            return Base().modulation_into_datagram_with_segment(ptr, segment)
        return Base().modulation_into_datagram_with_segment_transition(ptr, segment, transition_mode)

    @abstractmethod
    def _modulation_ptr(self: "ModulationBase[M]") -> ModulationPtr:
        pass

    def with_loop_behavior(self: M, loop_behavior: _LoopBehavior) -> M:
        self._loop_behavior = loop_behavior
        return self

    @property
    def loop_behavior(self: "ModulationBase[M]") -> _LoopBehavior:
        return self._loop_behavior

    @property
    def sampling_config(self: "ModulationBase[M]") -> SamplingConfig:
        return SamplingConfig(Base().modulation_sampling_config(self._modulation_ptr()))

    def _sampling_config_intensity(self: "ModulationBase[M]") -> SamplingConfig:
        return self.sampling_config

    def _sampling_config_phase(self: "ModulationBase[M]") -> SamplingConfig:
        return SamplingConfig(0xFFFF)
