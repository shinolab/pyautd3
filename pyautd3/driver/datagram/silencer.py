from datetime import timedelta
from typing import Generic, TypeVar

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.stm.foci import FociSTM
from pyautd3.driver.datagram.stm.gain import GainSTM
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.geometry import Geometry
from pyautd3.driver.utils import _validate_nonzero_u16
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, SilencerTarget

from .datagram import Datagram


class FixedCompletionTime:
    intensity: timedelta
    phase: timedelta

    def __init__(self: "FixedCompletionTime", *, intensity: timedelta, phase: timedelta) -> None:
        self.intensity = intensity
        self.phase = phase

    def _is_valid(
        self: "FixedCompletionTime",
        v: ModulationBase | FociSTM | GainSTM,
        strict_mode: bool,  # noqa: FBT001
        target: SilencerTarget,
    ) -> bool:
        return bool(
            Base().datagram_silencer_fixed_completion_time_is_valid(
                self._datagram_ptr(strict_mode, target),
                v._sampling_config_intensity()._inner,
                v._sampling_config_phase()._inner,
            ),
        )

    def _datagram_ptr(self: "FixedCompletionTime", strict_mode: bool, target: SilencerTarget) -> DatagramPtr:  # noqa: FBT001
        return Base().datagram_silencer_from_completion_time(
            int(self.intensity.total_seconds() * 1000 * 1000 * 1000),
            int(self.phase.total_seconds() * 1000 * 1000 * 1000),
            strict_mode,
            target,
        )


class FixedUpdateRate:
    intensity: int
    phase: int

    def __init__(self: "FixedUpdateRate", *, intensity: int, phase: int) -> None:
        self.intensity = _validate_nonzero_u16(intensity)
        self.phase = _validate_nonzero_u16(phase)

    def _is_valid(self: "FixedUpdateRate", v: ModulationBase | FociSTM | GainSTM, strict_mode: bool, target: SilencerTarget) -> bool:  # noqa: FBT001
        return bool(
            Base().datagram_silencer_fixed_update_rate_is_valid(
                self._datagram_ptr(strict_mode, target),
                v._sampling_config_intensity()._inner,
                v._sampling_config_phase()._inner,
            ),
        )

    def _datagram_ptr(self: "FixedUpdateRate", _strict_mode: bool, target: SilencerTarget) -> DatagramPtr:  # noqa: FBT001
        return Base().datagram_silencer_from_update_rate(
            self.intensity,
            self.phase,
            target,
        )


T = TypeVar("T", FixedCompletionTime, FixedUpdateRate)


class Silencer(
    IntoDatagramWithTimeout["Silencer"],
    IntoDatagramWithParallelThreshold["Silencer"],
    Datagram,
    Generic[T],
):
    _inner: T
    _strict_mode: bool
    _target: SilencerTarget

    def __init__(self: "Silencer[T]", config: T | None = None) -> None:
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
        self._target = SilencerTarget.Intensity

    def with_target(self: "Silencer[T]", target: SilencerTarget) -> "Silencer[T]":
        self._target = target
        return self

    def with_strict_mode(self: "Silencer[FixedCompletionTime]", mode: bool) -> "Silencer[FixedCompletionTime]":  # noqa: FBT001
        if not isinstance(self._inner, FixedCompletionTime):  # pragma: no cover
            msg = "Strict mode is only available for Silencer[FixedCompletionTime]"  # pragma: no cover
            raise TypeError(msg)  # pragma: no cover
        self._strict_mode = mode
        return self

    def is_valid(self: "Silencer[T]", target: ModulationBase | FociSTM | GainSTM) -> bool:
        return self._inner._is_valid(target, self._strict_mode, self._target)

    def _datagram_ptr(self: "Silencer[T]", _: Geometry) -> DatagramPtr:
        return self._inner._datagram_ptr(self._strict_mode, self._target)

    @staticmethod
    def disable() -> "Silencer[FixedCompletionTime]":
        return Silencer(FixedCompletionTime(intensity=timedelta(microseconds=25), phase=timedelta(microseconds=25)))
