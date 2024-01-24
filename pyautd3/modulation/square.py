from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.driver.common.sampling_config import SamplingConfiguration
from pyautd3.driver.datagram.modulation import IModulationWithSamplingConfig
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import SamplingMode
from pyautd3.native_methods.autd3capi_def import ModulationPtr


class Square(IModulationWithSamplingConfig):
    """Square wave modulation."""

    _freq: float
    _low: EmitIntensity
    _high: EmitIntensity
    _duty: float
    _mode: SamplingMode

    def __init__(self: "Square", freq: float) -> None:
        """Constructor.

        Arguments:
        ---------
            freq: Frequency (Hz)
        """
        super().__init__(SamplingConfiguration.from_frequency(4e3))
        self._freq = freq
        self._low = EmitIntensity.minimum()
        self._high = EmitIntensity.maximum()
        self._duty = 0.5
        self._mode = SamplingMode.ExactFrequency

    def freq(self: "Square") -> float:
        """Get frequency."""
        return self._freq

    def with_low(self: "Square", low: int | EmitIntensity) -> "Square":
        """Set low level intensity.

        Arguments:
        ---------
            low: Low level intensity
        """
        self._low = EmitIntensity._cast(low)
        return self

    def low(self: "Square") -> EmitIntensity:
        """Get low level intensity."""
        return self._low

    def with_high(self: "Square", high: int | EmitIntensity) -> "Square":
        """Set high level intensity.

        Arguments:
        ---------
            high: High level intensity
        """
        self._high = EmitIntensity._cast(high)
        return self

    def high(self: "Square") -> EmitIntensity:
        """Get high level intensity."""
        return self._high

    def with_duty(self: "Square", duty: float) -> "Square":
        """Set duty ratio which is defined as `Th / (Th + Tl)`, where `Th` is high level duration and `Tl` is low level duration.

        Arguments:
        ---------
            duty: Duty ratio (from 0 to 1)
        """
        self._duty = duty
        return self

    def duty(self: "Square") -> float:
        """Get duty ratio."""
        return self._duty

    def with_mode(self: "Square", mode: SamplingMode) -> "Square":
        """Set sampling mode.

        Arguments:
        ---------
            mode: Sampling mode
        """
        self._mode = mode
        return self

    def mode(self: "Square") -> SamplingMode:
        """Get sampling mode."""
        return self._mode

    def _modulation_ptr(self: "Square") -> ModulationPtr:
        return Base().modulation_square(
            self._freq,
            self._config._internal,
            self._low.value,
            self._high.value,
            self._duty,
            self._mode,
        )
