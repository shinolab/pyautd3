from typing import Generic, Self, TypeVar

from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.silencer.fixed_completion_steps import FixedCompletionSteps
from pyautd3.driver.datagram.silencer.fixed_completion_time import FixedCompletionTime
from pyautd3.driver.datagram.silencer.fixed_update_rate import FixedUpdateRate
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr

T = TypeVar("T", FixedCompletionSteps, FixedCompletionTime, FixedUpdateRate)


class Silencer(
    Datagram,
    Generic[T],
):
    config: T

    def __init__(self: Self, config: T | None = None) -> None:
        super().__init__()
        self.config = config or FixedCompletionSteps()  # type: ignore[assignment]

    def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
        match self.config:
            case FixedCompletionSteps():
                return Base().datagram_silencer_from_completion_steps(self.config._inner())
            case FixedCompletionTime():
                return Base().datagram_silencer_from_completion_time(self.config._inner())
            case FixedUpdateRate():  # pragma: no cover
                return Base().datagram_silencer_from_update_rate(self.config._inner())

    @staticmethod
    def disable() -> "Silencer[FixedCompletionSteps]":
        return Silencer(config=FixedCompletionSteps(intensity=1, phase=1))
