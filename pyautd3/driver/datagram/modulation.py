from abc import ABCMeta, abstractmethod
from typing import Self, TypeVar

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.with_loop_behavior import DatagramL
from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.firmware.fpga.transition_mode import TransitionMode
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3 import Segment
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, LoopBehavior, ModulationPtr, TransitionModeWrap

M = TypeVar("M", bound="Modulation")


class Modulation(
    DatagramS[ModulationPtr],
    DatagramL[ModulationPtr],
    Datagram,
    metaclass=ABCMeta,
):
    def __init__(self: Self) -> None:
        super().__init__()

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
            transition_mode or TransitionMode.NONE,
        )

    def _into_loop_behavior(
        self: Self,
        ptr: ModulationPtr,
        segment: Segment,
        transition_mode: TransitionModeWrap | None,
        loop_behavior: LoopBehavior,
    ) -> DatagramPtr:
        return Base().modulation_into_datagram_with_loop_behavior(
            ptr,
            segment,
            transition_mode or TransitionMode.NONE,
            loop_behavior,
        )

    @abstractmethod
    def _modulation_ptr(self: Self) -> ModulationPtr:
        pass

    def sampling_config(self: Self) -> SamplingConfig:
        return SamplingConfig(Base().modulation_sampling_config(self._modulation_ptr()))
