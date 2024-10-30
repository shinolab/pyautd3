from datetime import timedelta
from typing import Generic, Self, TypeVar

from pyautd3.derive import builder, datagram
from pyautd3.driver.datagram.datagram import Datagram
from pyautd3.driver.datagram.modulation import Modulation
from pyautd3.driver.datagram.silencer.fixed_completion_time import FixedCompletionTime
from pyautd3.driver.datagram.silencer.fixed_update_rate import FixedUpdateRate
from pyautd3.driver.datagram.stm.foci import FociSTM
from pyautd3.driver.datagram.stm.gain import GainSTM
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, SilencerTarget

T = TypeVar("T", FixedCompletionTime, FixedUpdateRate)


@builder
@datagram
class Silencer(
    Datagram,
    Generic[T],
):
    _inner: T
    _strict_mode: bool
    _param_target: SilencerTarget

    def __init__(self: Self, config: T | None = None) -> None:
        super().__init__()
        self._inner = (
            config
            if config is not None
            else FixedCompletionTime(
                intensity=timedelta(microseconds=250),
                phase=timedelta(microseconds=1000),
            )  # type: ignore[assignment]
        )
        self._strict_mode = True
        self._param_target = SilencerTarget.Intensity

    def with_strict_mode(self: "Silencer[T]", mode: bool) -> "Silencer[T]":  # noqa: FBT001
        if not isinstance(self._inner, FixedCompletionTime):  # pragma: no cover
            msg = "Strict mode is only available for Silencer[FixedCompletionTime]"  # pragma: no cover
            raise TypeError(msg)  # pragma: no cover
        self._strict_mode = mode
        return self

    def is_valid(self: Self, target: Modulation | FociSTM | GainSTM) -> bool:
        return self._inner._is_valid(target, self._strict_mode)

    def _datagram_ptr(self: Self, _: Geometry) -> DatagramPtr:
        return self._inner._datagram_ptr(self._strict_mode, self._param_target)

    @staticmethod
    def disable() -> "Silencer[FixedCompletionTime]":
        return Silencer(FixedCompletionTime(intensity=timedelta(microseconds=25), phase=timedelta(microseconds=25)))
