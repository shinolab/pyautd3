from abc import ABCMeta, abstractmethod
from typing import Self, TypeVar

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.with_finite_loop import DatagramL
from pyautd3.driver.datagram.with_segment import DatagramS
from pyautd3.driver.firmware.fpga.sampling_config import SamplingConfig
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3 import Segment
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, ModulationPtr, TransitionModeWrap

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
        transition_mode: TransitionModeWrap,
    ) -> DatagramPtr:
        return Base().modulation_into_datagram_with_segment(
            ptr,
            segment,
            transition_mode,
        )

    def _into_loop_behavior(
        self: Self,
        ptr: ModulationPtr,
        segment: Segment,
        transition_mode: TransitionModeWrap,
        loop_count: int,
    ) -> DatagramPtr:
        return Base().modulation_into_datagram_with_finite_loop(
            ptr,
            segment,
            transition_mode,
            loop_count,
        )

    @abstractmethod
    def _modulation_ptr(self: Self) -> ModulationPtr:
        pass

    def sampling_config(self: Self) -> SamplingConfig:
        return SamplingConfig(Base().modulation_sampling_config(self._modulation_ptr()))
