from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_driver import DatagramPtr
from pyautd3.native_methods.utils import _validate_ptr

from .datagram import Datagram


class Silencer(Datagram):
    class FixedUpdateRate(Datagram):
        _value_intensity: int
        _value_phase: int

        def __init__(self: "Silencer.FixedUpdateRate", value_intensity: int, value_phase: int) -> None:
            super().__init__()
            self._value_intensity = value_intensity
            self._value_phase = value_phase

        def _datagram_ptr(self: "Silencer.FixedUpdateRate", _: Geometry) -> DatagramPtr:
            return _validate_ptr(Base().datagram_silencer_fixed_update_rate(self._value_intensity, self._value_phase))

    class FixedCompletionSteps(Datagram):
        _value_intensity: int
        _value_phase: int
        _strict_mode: bool

        def __init__(self: "Silencer.FixedCompletionSteps", value_intensity: int, value_phase: int) -> None:
            super().__init__()
            self._value_intensity = value_intensity
            self._value_phase = value_phase
            self._strict_mode = True

        def with_strict_mode(self: "Silencer.FixedCompletionSteps", mode: bool) -> "Silencer.FixedCompletionSteps":  # noqa: FBT001
            self._strict_mode = mode
            return self

        def _datagram_ptr(self: "Silencer.FixedCompletionSteps", _: Geometry) -> DatagramPtr:
            return _validate_ptr(
                Base().datagram_silencer_fixed_completion_steps(
                    self._value_intensity,
                    self._value_phase,
                    self._strict_mode,
                ),
            )

    @staticmethod
    def fixed_update_rate(value_intensity: int, value_phase: int) -> "FixedUpdateRate":
        return Silencer.FixedUpdateRate(value_intensity, value_phase)

    @staticmethod
    def fixed_completion_steps(value_intensity: int, value_phase: int) -> "FixedCompletionSteps":
        return Silencer.FixedCompletionSteps(value_intensity, value_phase)

    @staticmethod
    def disable() -> "FixedCompletionSteps":
        return Silencer.fixed_completion_steps(1, 1)

    @staticmethod
    def default() -> "FixedCompletionSteps":
        return Silencer.fixed_completion_steps(10, 40)
