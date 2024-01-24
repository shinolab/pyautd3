from pyautd3.driver.geometry import Geometry
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi_def import DatagramPtr
from pyautd3.native_methods.utils import _validate_ptr

from .datagram import Datagram


class ConfigureSilencer(Datagram):
    """Datagram for configure silencer."""

    class FixedUpdateRate(Datagram):
        """Datagram for configure silencer with fixed update rate."""

        _value_intensity: int
        _value_phase: int

        def __init__(self: "ConfigureSilencer.FixedUpdateRate", value_intensity: int, value_phase: int) -> None:
            """Constructor.

            Arguments:
            ---------
                value_intensity: The intensity update rate of silencer. The lower the value, the stronger the silencer effect.
                value_phase: The phase update rate of silencer. The lower the value, the stronger the silencer effect.
            """
            super().__init__()
            self._value_intensity = value_intensity
            self._value_phase = value_phase

        def _datagram_ptr(self: "ConfigureSilencer.FixedUpdateRate", _: Geometry) -> DatagramPtr:
            return _validate_ptr(Base().datagram_silencer_fixed_update_rate(self._value_intensity, self._value_phase))

    class FixedCompletionSteps(Datagram):
        """Datagram for configure silencer with fixed completion steps."""

        _value_intensity: int
        _value_phase: int
        _strict_mode: bool

        def __init__(self: "ConfigureSilencer.FixedCompletionSteps", value_intensity: int, value_phase: int) -> None:
            """Constructor.

            Arguments:
            ---------
                value_intensity: The intensity completion steps of silencer. The larger the value, the stronger the silencer effect.
                value_phase: The phase completion steps of silencer. The larger the value, the stronger the silencer effect.
            """
            super().__init__()
            self._value_intensity = value_intensity
            self._value_phase = value_phase
            self._strict_mode = True

        def with_strict_mode(self: "ConfigureSilencer.FixedCompletionSteps", *, mode: bool) -> "ConfigureSilencer.FixedCompletionSteps":
            """Set strict mode.

            Arguments:
            ---------
                mode: If true, the invalid completion steps will cause an error.
            """
            self._strict_mode = mode
            return self

        def _datagram_ptr(self: "ConfigureSilencer.FixedCompletionSteps", _: Geometry) -> DatagramPtr:
            return _validate_ptr(
                Base().datagram_silencer_fixed_completion_steps(
                    self._value_intensity,
                    self._value_phase,
                    self._strict_mode,
                ),
            )

    @staticmethod
    def fixed_update_rate(value_intensity: int, value_phase: int) -> "FixedUpdateRate":
        """Fixed update rate silencer.

        Arguments:
        ---------
            value_intensity: The intensity update rate of silencer. The lower the value, the stronger the silencer effect.
            value_phase: The phase update rate of silencer. The lower the value, the stronger the silencer effect.
        """
        return ConfigureSilencer.FixedUpdateRate(value_intensity, value_phase)

    @staticmethod
    def fixed_completion_steps(value_intensity: int, value_phase: int) -> "FixedCompletionSteps":
        """Fixed completion steps silencer.

        Arguments:
        ---------
            value_intensity: The intensity completion steps of silencer. The larger the value, the stronger the silencer effect.
            value_phase: The phase completion steps of silencer. The larger the value, the stronger the silencer effect.
        """
        return ConfigureSilencer.FixedCompletionSteps(value_intensity, value_phase)

    @staticmethod
    def disable() -> "FixedCompletionSteps":
        """Disable silencer."""
        return ConfigureSilencer.fixed_completion_steps(1, 1)

    @staticmethod
    def default() -> "FixedCompletionSteps":
        """Default silencer."""
        return ConfigureSilencer.fixed_completion_steps(10, 40)
