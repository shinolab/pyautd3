from pyautd3.driver.common.emit_intensity import EmitIntensity
from pyautd3.driver.common.phase import Phase
from pyautd3.driver.common.sampling_config import SamplingConfiguration
from pyautd3.driver.datagram.modulation import IModulationWithSamplingConfig
from pyautd3.native_methods.autd3capi import NativeMethods as Base
from pyautd3.native_methods.autd3capi import SamplingMode
from pyautd3.native_methods.autd3capi_def import ModulationPtr


class Sine(IModulationWithSamplingConfig):
    """Sine wave modulation."""

    _freq: float
    _intensity: EmitIntensity
    _offset: EmitIntensity
    _phase: Phase
    _mode: SamplingMode

    def __init__(self: "Sine", freq: float) -> None:
        """Constructor.

        The sine wave is defined as `amp/2 * sin(2π * freq * t + phase) + offset`,
        where `t` is time, and `amp = EmitIntensity.maximum()`, `phase = 0`, `offset = EmitIntensity.maximum()/2` by default.

        Arguments:
        ---------
            freq: Frequency (Hz)
        """
        super().__init__(SamplingConfiguration.from_frequency(4e3))
        self._freq = freq
        self._intensity = EmitIntensity.maximum()
        self._offset = EmitIntensity.maximum() // 2
        self._phase = Phase(0)
        self._mode = SamplingMode.ExactFrequency

    def freq(self: "Sine") -> float:
        """Get frequency."""
        return self._freq

    def with_intensity(self: "Sine", intensity: int | EmitIntensity) -> "Sine":
        """Set intensity.

        Arguments:
        ---------
            intensity: Intensity
        """
        self._intensity = EmitIntensity._cast(intensity)
        return self

    def intensity(self: "Sine") -> EmitIntensity:
        """Get intensity."""
        return self._intensity

    def with_offset(self: "Sine", offset: int | EmitIntensity) -> "Sine":
        """Set offset.

        Arguments:
        ---------
            offset: Offset
        """
        self._offset = EmitIntensity._cast(offset)
        return self

    def offset(self: "Sine") -> EmitIntensity:
        """Get offset."""
        return self._offset

    def with_phase(self: "Sine", phase: Phase) -> "Sine":
        """Set phase.

        Arguments:
        ---------
            phase: Phase
        """
        self._phase = phase
        return self

    def phase(self: "Sine") -> Phase:
        """Get phase."""
        return self._phase

    def with_mode(self: "Sine", mode: SamplingMode) -> "Sine":
        """Set sampling mode.

        Arguments:
        ---------
            mode: Sampling mode
        """
        self._mode = mode
        return self

    def mode(self: "Sine") -> SamplingMode:
        """Get sampling mode."""
        return self._mode

    def _modulation_ptr(self: "Sine") -> ModulationPtr:
        return Base().modulation_sine(
            self._freq,
            self._config._internal,
            self._intensity.value,
            self._offset.value,
            self._phase.value,
            self._mode,
        )
