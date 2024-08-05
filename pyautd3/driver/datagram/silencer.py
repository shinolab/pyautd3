from datetime import timedelta

from pyautd3.driver.datagram.modulation.base import ModulationBase
from pyautd3.driver.datagram.stm.foci import FociSTM
from pyautd3.driver.datagram.stm.gain import GainSTM
from pyautd3.driver.datagram.with_parallel_threshold import IntoDatagramWithParallelThreshold
from pyautd3.driver.datagram.with_timeout import IntoDatagramWithTimeout
from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr, SilencerTarget

from .datagram import Datagram


class Silencer(
    IntoDatagramWithTimeout["Silencer"],
    IntoDatagramWithParallelThreshold["Silencer"],
    Datagram,
):
    class FixedUpdateRate(
        IntoDatagramWithTimeout["Silencer.FixedUpdateRate"],
        IntoDatagramWithParallelThreshold["Silencer.FixedUpdateRate"],
        Datagram,
    ):
        _value_intensity: int
        _value_phase: int
        _target: SilencerTarget

        def __init__(self: "Silencer.FixedUpdateRate", value_intensity: int, value_phase: int) -> None:
            super().__init__()
            self._value_intensity = value_intensity
            self._value_phase = value_phase
            self._target = SilencerTarget.Intensity

        def with_target(self: "Silencer.FixedUpdateRate", target: SilencerTarget) -> "Silencer.FixedUpdateRate":
            self._target = target
            return self

        def _datagram_ptr(self: "Silencer.FixedUpdateRate", _: Geometry) -> DatagramPtr:
            return Base().datagram_silencer_from_update_rate(
                self._value_intensity,
                self._value_phase,
                self._target,
            )

        def is_valid(self: "Silencer.FixedUpdateRate", target: ModulationBase | FociSTM | GainSTM) -> bool:
            return bool(
                Base().datagram_silencer_fixed_update_rate_is_valid(
                    self._datagram_ptr(None),  # type: ignore[arg-type]
                    target._sampling_config_intensity()._inner,
                    target._sampling_config_phase()._inner,
                ),
            )

    class FixedCompletionTime(Datagram):
        _value_intensity: timedelta
        _value_phase: timedelta
        _strict_mode: bool
        _target: SilencerTarget

        def __init__(self: "Silencer.FixedCompletionTime", value_intensity: timedelta, value_phase: timedelta) -> None:
            super().__init__()
            self._value_intensity = value_intensity
            self._value_phase = value_phase
            self._strict_mode = True
            self._target = SilencerTarget.Intensity

        def with_target(self: "Silencer.FixedCompletionTime", target: SilencerTarget) -> "Silencer.FixedCompletionTime":
            self._target = target
            return self

        def with_strict_mode(self: "Silencer.FixedCompletionTime", mode: bool) -> "Silencer.FixedCompletionTime":  # noqa: FBT001
            self._strict_mode = mode
            return self

        def _datagram_ptr(self: "Silencer.FixedCompletionTime", _: Geometry) -> DatagramPtr:
            return Base().datagram_silencer_from_completion_time(
                int(self._value_intensity.total_seconds() * 1000 * 1000 * 1000),
                int(self._value_phase.total_seconds() * 1000 * 1000 * 1000),
                self._strict_mode,
                self._target,
            )

        def is_valid(self: "Silencer.FixedCompletionTime", target: ModulationBase | FociSTM | GainSTM) -> bool:
            return bool(
                Base().datagram_silencer_fixed_completion_time_is_valid(
                    self._datagram_ptr(None),  # type: ignore[arg-type]
                    target._sampling_config_intensity()._inner,
                    target._sampling_config_phase()._inner,
                ),
            )

    @staticmethod
    def from_update_rate(value_intensity: int, value_phase: int) -> "FixedUpdateRate":
        return Silencer.FixedUpdateRate(value_intensity, value_phase)

    @staticmethod
    def from_completion_time(value_intensity: timedelta, value_phase: timedelta) -> "FixedCompletionTime":
        return Silencer.FixedCompletionTime(value_intensity, value_phase)

    @staticmethod
    def disable() -> "FixedCompletionTime":
        return Silencer.from_completion_time(timedelta(microseconds=25), timedelta(microseconds=25))

    @staticmethod
    def default() -> "FixedCompletionTime":
        return Silencer.from_completion_time(timedelta(microseconds=250), timedelta(microseconds=1000))
