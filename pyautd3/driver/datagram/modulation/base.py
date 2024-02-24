from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from pyautd3.driver.common import LoopBehavior, SamplingConfiguration
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.with_segment import DatagramS, IntoDatagramWithSegment
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr, ModulationPtr, Segment
from pyautd3.native_methods.utils import _validate_int

__all__ = []  # type: ignore[var-annotated]

M = TypeVar("M", bound="ModulationBase")


class ModulationBase(IntoDatagramWithSegment[M], DatagramS[ModulationPtr], Generic[M], metaclass=ABCMeta):
    _loop_behavior: LoopBehavior

    def __init__(self: "ModulationBase[M]") -> None:
        super().__init__()
        self._loop_behavior = LoopBehavior.infinite()

    def _raw_ptr(self: "ModulationBase[M]", _: Geometry) -> ModulationPtr:
        return self._modulation_ptr()

    def _into_segment(self: "ModulationBase[M]", ptr: ModulationPtr, segment: tuple[Segment, bool] | None) -> DatagramPtr:
        if segment is None:
            return Base().modulation_into_datagram(ptr)
        segment_, update_segment = segment
        return Base().modulation_into_datagram_with_segment(ptr, segment_, update_segment)

    @property
    def sampling_config(self: "ModulationBase[M]") -> SamplingConfiguration:
        return SamplingConfiguration.__private_new__(Base().modulation_sampling_config(self._modulation_ptr()))

    def __len__(self: "ModulationBase[M]") -> int:
        return _validate_int(Base().modulation_size(self._modulation_ptr()))

    @abstractmethod
    def _modulation_ptr(self: "ModulationBase[M]") -> ModulationPtr:
        pass

    def with_loop_behavior(self: M, loop_behavior: LoopBehavior) -> M:
        """Set loop behavior.

        Arguments:
        ---------
            loop_behavior: Loop behavior.

        """
        self._loop_behavior = loop_behavior
        return self

    @property
    def loop_behavior(self: "ModulationBase[M]") -> LoopBehavior:
        """Get loop behavior."""
        return self._loop_behavior


class ChangeModulationSegment(Datagram):
    _segment: Segment

    def __init__(self: "ChangeModulationSegment", segment: Segment) -> None:
        super().__init__()
        self._segment = segment

    def _datagram_ptr(self: "ChangeModulationSegment", _: Geometry) -> DatagramPtr:
        return Base().datagram_change_modulation_segment(self._segment)
